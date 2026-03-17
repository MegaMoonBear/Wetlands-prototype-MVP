Seed data that (1) respects relationships across tables and (2) is easy to drop into Thunder Client / EchoAPI without fighting UUID generation (by using **fixed UUIDs** so you can reliably test joins).

---

## 1. Seed: `observations`

```sql
INSERT INTO observations (
    id, observed_at, data_source, user_UUID,
    tags_user_device, tags_AI_ConfidL,
    tag_OptionONLY_P1, validation_status,
    validation_reject, is_deleted
)
VALUES
(
    '11111111-1111-1111-1111-111111111111',
    '2026-03-10T14:23:00Z',
    'mobile_app',
    'user_001',
    ARRAY['bird','outdoor','tree'],
    '0.92',
    'cardinal',
    'pending',
    NULL,
    FALSE
),
(
    '22222222-2222-2222-2222-222222222222',
    '2026-03-11T09:12:00Z',
    'web_upload',
    'user_002',
    ARRAY['water','reflection'],
    '0.87',
    'lake',
    'approved',
    NULL,
    FALSE
),
(
    '33333333-3333-3333-3333-333333333333',
    '2026-03-12T18:45:00Z',
    'mobile_app',
    'user_003',
    ARRAY['animal','night'],
    '0.65',
    'raccoon',
    'rejected',
    'blurry_image',
    FALSE
);
```

---

## 2. Seed: `media`

```sql
INSERT INTO media (
    id, observation_UUID, media_type,
    metadata_extracted, storage_url, storage_path
)
VALUES
(
    'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1',
    '11111111-1111-1111-1111-111111111111',
    'image/jpeg',
    TRUE,
    'https://cdn.example.com/images/cardinal1.jpg',
    '/uploads/cardinal1.jpg'
),
(
    'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2',
    '22222222-2222-2222-2222-222222222222',
    'image/jpeg',
    TRUE,
    'https://cdn.example.com/images/lake1.jpg',
    '/uploads/lake1.jpg'
),
(
    'aaaaaaa3-aaaa-aaaa-aaaa-aaaaaaaaaaa3',
    '33333333-3333-3333-3333-333333333333',
    'image/png',
    FALSE,
    'https://cdn.example.com/images/raccoon1.png',
    '/uploads/raccoon1.png'
);
```

---

## 3. Seed: `pic_metadata_exif`

```sql
INSERT INTO pic_metadata_exif (
    media_id,
    datetime_original,
    latitude,
    longitude,
    altitude,
    compass_direction,
    orientation,
    additional_metadata
)
VALUES
(
    'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1',
    '2026-03-10 14:22:10',
    35.3859,
    -94.3985,
    140.5,
    180.0,
    '1',
    '{"camera":"iPhone 13","iso":100,"exposure":"1/200"}'
),
(
    'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2',
    '2026-03-11 09:10:05',
    34.7465,
    -92.2896,
    90.2,
    75.0,
    '1',
    '{"camera":"Canon EOS R","lens":"24-70mm","iso":200}'
),
(
    'aaaaaaa3-aaaa-aaaa-aaaa-aaaaaaaaaaa3',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    '{"note":"metadata not extracted yet"}'
);
```

---

## Why this setup works (don’t skip this)

* **Deterministic UUIDs** → makes debugging joins easy
* **Covers edge cases**:

  * approved vs rejected vs pending
  * metadata extracted vs not
  * missing EXIF values
* **Realistic relationships**:

  * 1 observation → 1 media (you can expand later to many)
  * media → optional EXIF

---

## If you want to level this up (worth doing next)

Right now your schema is solid, but a couple upgrades will save you pain later:

1. **Change `tags_AI_ConfidL` to FLOAT**

   * You’re storing numbers as TEXT → that will hurt filtering later

2. Consider adding:

```sql
created_at TIMESTAMP DEFAULT NOW()
updated_at TIMESTAMP DEFAULT NOW()
```

3. If you expect multiple media per observation (you probably will):

* keep this structure, you're already set 👍

---

If you want, I can generate:

* a **Postman / Thunder Client collection JSON**
* or a **seed script that runs in order with rollback support**

That’s usually the next step once this data looks right.
