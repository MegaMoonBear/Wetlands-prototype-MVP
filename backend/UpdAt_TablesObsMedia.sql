CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_updated_at
BEFORE UPDATE ON observations
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trigger_set_updated_at_media
BEFORE UPDATE ON media
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();