#!/usr/bin/env python3
import base64, json, os, subprocess, tempfile, sys, re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image

MAX = 128 * 1024 * 1024

def run(cmd, timeout=170):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)

class H(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write("[HTTP] %s - %s\n" % (self.address_string(), format % args))
        sys.stderr.flush()

    def sendj(self, status, data):
        try:
            b = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        if self.path == "/health":
            self.sendj(200, {"ok": True, "engine": "tesseract-5.5.0"})
        else:
            self.sendj(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/ocr":
            return self.sendj(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n < 1 or n > MAX * 2:
                raise ValueError("invalid request size %d" % n)
            body = json.loads(self.rfile.read(n).decode("utf-8", "replace"))
            raw = base64.b64decode(body.get("pdf_base64", ""), validate=False)
            if not raw or len(raw) > MAX:
                raise ValueError("invalid pdf payload size=%d" % (len(raw) if raw else 0))

            with tempfile.TemporaryDirectory(prefix="cic-ocr-") as d:
                src = os.path.join(d, "source.pdf")
                with open(src, "wb") as f:
                    f.write(raw)

                # 1. Fast digital text extraction
                p_text = run(["pdftotext", "-layout", src, "-"], 60)
                text = p_text.stdout.decode("utf-8", "replace").strip()
                if len(text) >= 40:
                    sys.stderr.write("[OCR] Extracted %d chars via pdftotext\n" % len(text))
                    sys.stderr.flush()
                    return self.sendj(200, {"text": text, "engine": "pdftotext"})

                # 2. Poppler rendering + Tesseract
                r = run(["pdftoppm", "-r", "150", "-png", src, os.path.join(d, "page")], 120)
                if r.returncode != 0:
                    err_str = r.stderr.decode("utf-8", "replace")[:500]
                    sys.stderr.write("[OCR ERROR] pdftoppm failed: %s\n" % err_str)
                    sys.stderr.flush()
                    raise RuntimeError("pdftoppm: %s" % err_str)

                pages = sorted(os.path.join(d, x) for x in os.listdir(d) if x.startswith("page-") and x.endswith(".png"))
                if not pages:
                    return self.sendj(200, {"text": "", "engine": "tesseract-5.5.0"})

                out = []
                for p in pages:
                    try:
                        with Image.open(p) as im:
                            w, h = im.size
                        # Only run OSD if landscape orientation (w >= h)
                        if w >= h:
                            osd_res = run(["tesseract", p, "stdout", "--psm", "0"], 15)
                            osd_out = osd_res.stdout.decode("utf-8", "replace")
                            m_rot = re.search(r"Rotate:\s*(\d+)", osd_out)
                            m_conf = re.search(r"Orientation confidence:\s*([\d.]+)", osd_out)
                            rot = int(m_rot.group(1)) if m_rot else 0
                            conf = float(m_conf.group(1)) if m_conf else 0.0

                            if rot in (90, 180, 270) and conf >= 1.0:
                                pil_deg = (360 - rot) % 360
                                with Image.open(p) as im:
                                    im_rot = im.rotate(pil_deg, expand=True)
                                    im_rot.save(p)
                                sys.stderr.write("[OCR ROTATE] %s rotated by %d deg (OSD rot=%d, conf=%.1f)\n" % (os.path.basename(p), pil_deg, rot, conf))
                                sys.stderr.flush()
                    except Exception as rot_err:
                        sys.stderr.write("[OCR ROTATE WARNING] %s\n" % str(rot_err))
                        sys.stderr.flush()

                    # Standard line-by-line block OCR
                    tr = run(["tesseract", p, "stdout", "-l", "vie+eng", "--psm", "6"], 120)
                    page_text = tr.stdout.decode("utf-8", "replace").strip() if tr.returncode == 0 else ""

                    if len(page_text) < 40:
                        tr3 = run(["tesseract", p, "stdout", "-l", "vie+eng", "--psm", "3"], 120)
                        if tr3.returncode == 0:
                            fb_text = tr3.stdout.decode("utf-8", "replace").strip()
                            if len(fb_text) > len(page_text):
                                page_text = fb_text

                    if page_text:
                        out.append(page_text)

                result_text = "\n\n".join(x for x in out if x).strip()
                sys.stderr.write("[OCR] Extracted %d chars from %d pages via Tesseract\n" % (len(result_text), len(pages)))
                sys.stderr.flush()
                self.sendj(200, {"text": result_text, "engine": "tesseract-5.5.0"})

        except Exception as e:
            sys.stderr.write("[OCR EXCEPTION] %s\n" % str(e))
            sys.stderr.flush()
            self.sendj(422, {"error": str(e)[:500]})

if __name__ == "__main__":
    server = ThreadingHTTPServer(("172.18.0.1", 18710), H)
    sys.stderr.write("[OCR] Server listening on 172.18.0.1:18710\n")
    sys.stderr.flush()
    server.serve_forever()
