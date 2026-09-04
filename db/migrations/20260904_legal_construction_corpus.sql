SET LOCAL lock_timeout = '5s';
SET LOCAL statement_timeout = '60s';

CREATE TABLE IF NOT EXISTS public.legal_documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL,
  document_type text NOT NULL DEFAULT 'construction_legal_document',
  title text NOT NULL,
  document_number text,
  issuing_authority text,
  jurisdiction text NOT NULL DEFAULT 'VN',
  issued_date date,
  effective_date date,
  expiry_date date,
  legal_status text NOT NULL DEFAULT 'unknown' CHECK (legal_status IN ('unknown','effective','expired','repealed','superseded')),
  language_code text NOT NULL DEFAULT 'vi',
  source_type text NOT NULL DEFAULT 'google_drive',
  source_external_id text NOT NULL,
  source_url text,
  file_name text,
  mime_type text,
  content_hash text NOT NULL,
  status text NOT NULL DEFAULT 'processing' CHECK (status IN ('processing','active','failed','archived')),
  is_official boolean NOT NULL DEFAULT false,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, source_type, source_external_id),
  UNIQUE (id, organization_id)
);

CREATE TABLE IF NOT EXISTS public.legal_document_versions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id uuid NOT NULL,
  organization_id uuid NOT NULL,
  version_number integer NOT NULL CHECK (version_number > 0),
  source_content_hash text NOT NULL,
  extracted_text text,
  normalized_text text,
  parse_status text NOT NULL DEFAULT 'pending' CHECK (parse_status IN ('pending','processing','completed','failed')),
  chunk_status text NOT NULL DEFAULT 'pending' CHECK (chunk_status IN ('pending','processing','completed','failed')),
  embedding_status text NOT NULL DEFAULT 'pending' CHECK (embedding_status IN ('pending','processing','completed','failed')),
  index_status text NOT NULL DEFAULT 'pending' CHECK (index_status IN ('pending','processing','completed','failed')),
  is_current boolean NOT NULL DEFAULT false,
  extraction_method text,
  extracted_fields jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(extracted_fields) = 'object'),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (document_id, version_number),
  UNIQUE (document_id, source_content_hash),
  UNIQUE (id, organization_id),
  FOREIGN KEY (document_id, organization_id) REFERENCES public.legal_documents(id, organization_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS legal_document_versions_one_current_idx
  ON public.legal_document_versions(document_id) WHERE is_current;

CREATE TABLE IF NOT EXISTS public.legal_document_chunks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  document_version_id uuid NOT NULL,
  organization_id uuid NOT NULL,
  chunk_index integer NOT NULL CHECK (chunk_index >= 0),
  section text,
  article_ref text,
  page_start integer CHECK (page_start IS NULL OR page_start > 0),
  page_end integer CHECK (page_end IS NULL OR page_end >= page_start),
  title text,
  content text NOT NULL,
  normalized_content text,
  language_code text NOT NULL DEFAULT 'vi',
  token_count integer CHECK (token_count IS NULL OR token_count >= 0),
  content_hash text NOT NULL,
  search_vector tsvector GENERATED ALWAYS AS (to_tsvector('simple', coalesce(title,'') || ' ' || coalesce(section,'') || ' ' || coalesce(content,''))) STORED,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (document_version_id, chunk_index),
  UNIQUE (id, organization_id),
  FOREIGN KEY (document_version_id, organization_id) REFERENCES public.legal_document_versions(id, organization_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public.legal_chunk_embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  chunk_id uuid NOT NULL,
  organization_id uuid NOT NULL,
  embedding_model_id uuid NOT NULL REFERENCES public.embedding_models(id),
  embedding vector(1024) NOT NULL,
  content_hash text NOT NULL,
  is_active boolean NOT NULL DEFAULT true,
  is_retrievable boolean NOT NULL DEFAULT false,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (chunk_id, embedding_model_id, content_hash),
  FOREIGN KEY (chunk_id, organization_id) REFERENCES public.legal_document_chunks(id, organization_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public.legal_ingestion_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL,
  operation_key text NOT NULL UNIQUE,
  source_external_id text NOT NULL,
  source_content_hash text NOT NULL,
  document_id uuid REFERENCES public.legal_documents(id) ON DELETE SET NULL,
  document_version_id uuid REFERENCES public.legal_document_versions(id) ON DELETE SET NULL,
  status text NOT NULL DEFAULT 'processing' CHECK (status IN ('processing','skipped','completed','failed')),
  attempt_count integer NOT NULL DEFAULT 1 CHECK (attempt_count > 0),
  error_code text,
  error_message text,
  started_at timestamptz NOT NULL DEFAULT now(),
  completed_at timestamptz,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
  updated_at timestamptz NOT NULL DEFAULT now()
  ,FOREIGN KEY (document_id, organization_id) REFERENCES public.legal_documents(id, organization_id) ON DELETE SET NULL
  ,FOREIGN KEY (document_version_id, organization_id) REFERENCES public.legal_document_versions(id, organization_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS legal_documents_org_status_idx
  ON public.legal_documents(organization_id, status, is_official);
CREATE INDEX IF NOT EXISTS legal_documents_number_idx
  ON public.legal_documents(organization_id, document_number) WHERE document_number IS NOT NULL;
CREATE INDEX IF NOT EXISTS legal_document_versions_document_idx
  ON public.legal_document_versions(document_id, version_number DESC);
CREATE INDEX IF NOT EXISTS legal_document_chunks_org_version_idx
  ON public.legal_document_chunks(organization_id, document_version_id, chunk_index);
CREATE INDEX IF NOT EXISTS legal_document_chunks_search_idx
  ON public.legal_document_chunks USING gin(search_vector);
CREATE INDEX IF NOT EXISTS legal_chunk_embeddings_model_idx
  ON public.legal_chunk_embeddings(embedding_model_id);
CREATE INDEX IF NOT EXISTS legal_chunk_embeddings_hnsw_cosine_idx
  ON public.legal_chunk_embeddings USING hnsw (embedding vector_cosine_ops)
  WHERE is_active AND is_retrievable;
CREATE INDEX IF NOT EXISTS legal_ingestion_runs_org_status_idx
  ON public.legal_ingestion_runs(organization_id, status, updated_at DESC);

CREATE OR REPLACE FUNCTION public.legal_touch_updated_at()
RETURNS trigger LANGUAGE plpgsql SET search_path = public AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS legal_documents_touch_updated_at ON public.legal_documents;
CREATE TRIGGER legal_documents_touch_updated_at BEFORE UPDATE ON public.legal_documents
FOR EACH ROW EXECUTE FUNCTION public.legal_touch_updated_at();
DROP TRIGGER IF EXISTS legal_document_versions_touch_updated_at ON public.legal_document_versions;
CREATE TRIGGER legal_document_versions_touch_updated_at BEFORE UPDATE ON public.legal_document_versions
FOR EACH ROW EXECUTE FUNCTION public.legal_touch_updated_at();
DROP TRIGGER IF EXISTS legal_ingestion_runs_touch_updated_at ON public.legal_ingestion_runs;
CREATE TRIGGER legal_ingestion_runs_touch_updated_at BEFORE UPDATE ON public.legal_ingestion_runs
FOR EACH ROW EXECUTE FUNCTION public.legal_touch_updated_at();

ALTER TABLE public.legal_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legal_documents FORCE ROW LEVEL SECURITY;
ALTER TABLE public.legal_document_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legal_document_versions FORCE ROW LEVEL SECURITY;
ALTER TABLE public.legal_document_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legal_document_chunks FORCE ROW LEVEL SECURITY;
ALTER TABLE public.legal_chunk_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legal_chunk_embeddings FORCE ROW LEVEL SECURITY;
ALTER TABLE public.legal_ingestion_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legal_ingestion_runs FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.legal_documents, public.legal_document_versions, public.legal_document_chunks, public.legal_chunk_embeddings, public.legal_ingestion_runs FROM anon, authenticated;
GRANT ALL ON public.legal_documents, public.legal_document_versions, public.legal_document_chunks, public.legal_chunk_embeddings, public.legal_ingestion_runs TO service_role;

DO $$
DECLARE table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY['legal_documents','legal_document_versions','legal_document_chunks','legal_chunk_embeddings','legal_ingestion_runs']
  LOOP
    IF NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.schemaname='public' AND p.tablename=table_name AND p.policyname=table_name || '_service_role_all') THEN
      EXECUTE format('CREATE POLICY %I ON public.%I FOR ALL TO service_role USING (true) WITH CHECK (true)', table_name || '_service_role_all', table_name);
    END IF;
  END LOOP;
END;
$$;

COMMENT ON TABLE public.legal_documents IS 'Organization-wide official legal and regulatory documents; never product-scoped.';
COMMENT ON TABLE public.legal_document_versions IS 'Immutable source versions; only a fully completed version may be current.';
COMMENT ON TABLE public.legal_document_chunks IS 'Derived legal text chunks with page/article lineage.';
COMMENT ON TABLE public.legal_chunk_embeddings IS 'Derived 1024-dimensional L2-normalized legal chunk embeddings.';
COMMENT ON TABLE public.legal_ingestion_runs IS 'Durable idempotency and outcome records for Drive legal ingestion.';
