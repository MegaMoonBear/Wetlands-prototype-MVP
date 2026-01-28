**Lookup tables, instead of ENUM from Phase 2**
### Future Improvements
- Replace ENUMs in the database schema with lookup tables for better scalability, regional flexibility, and integration with external GIS layers.


## ✅ Recommendation: **Lookup tables (with optional mappings to NLCD / OSM / zoning)**

If you’re thinking **long-term**, **multi-region**, **partner-facing**, and **science-adjacent**, ENUMs will box you in. Lookup tables scale; ENUMs don’t.

---

## Why ENUMs break down over time

ENUMs are fine when:

* Categories are **fixed**
* You control **all inputs**
* You don’t expect **regional variation**

Your project fails all three 😄 (in a good way).

Problems you’ll hit:

* Schema migrations for every new category
* Regional categories that don’t fit (tribal land, conservation easements, easement overlays, etc.)
* Harder integration with **external GIS layers**
* Painful analytics when categories evolve

---

## Why lookup tables win

### 1️⃣ **Scalability**

You can add new categories **without touching the schema**.

```sql
land_use (
  id,
  code,
  label,
  description,
  parent_id
)
```

This supports:

* Hierarchies (`agriculture → crops → row_crops`)
* Future subcategories
* Region-specific extensions

---

### 2️⃣ **Interoperability with GIS Standards**

Lookup tables let you **map**, not hard-code.

```sql
land_use_mapping (
  land_use_id,
  source_system,   -- NLCD, OSM, Zoning
  source_code
)
```

Now you can:

* Ingest NLCD rasters
* Align with OpenStreetMap tags
* Translate local zoning codes cleanly

ENUMs cannot do this without hacks.

---

### 3️⃣ **Versioning & Scientific Credibility**

You can track:

* When categories changed
* Why they changed
* What data used the old version

That matters if:

* Researchers reuse your data
* Agencies ask about methodology
* You publish or apply for grants

---

### 4️⃣ **User-Facing Flexibility**

You can:

* Display friendly labels
* Keep internal codes stable
* Localize language later (schools, community partners)

ENUMs lock UI and data together.

---

## Best-Practice Hybrid Model (What I’d Actually Build)

**Use lookup tables as the source of truth**, then optionally expose a *small, stable subset* as enums in the API layer *only if needed* for validation.

### Core Tables

* `spatial_context`
* `ownership_type`
* `land_use`
* `environmental_designation`

Each with:

* `id`
* `code` (stable)
* `label` (human-readable)
* `description`
* `active` flag

### Mapping Tables

* `*_external_mapping` (NLCD / OSM / zoning)

---

## What to tell stakeholders (one-liner)

> “We use lookup tables so the system can evolve with new regions, policies, and conservation science without breaking the database.”

That line plays **very well** with:

* GIS teams
* Conservation orgs
* Civic data funders
* Engineers who think ahead

---

### Bottom line (direct)

If this app has *any* ambition beyond a pilot:
**lookup tables now will save you painful refactors later**.

If you want, next I can:

* sketch a **minimal SQL schema**
* show how to migrate safely from ENUMs
* or design a **taxonomy hierarchy** tuned specifically to wetlands & water systems


