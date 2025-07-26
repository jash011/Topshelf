# Ziplink – Concept Map

**Ziplink** Django URL shortener project  key concepts categorized by **Objects**, **Contexts**, and **Contextual Information**.

---

## Objects

### 1. **Link (Model)**

- Represents each shortened URL.
- Fields: `original_url`, `short_url`, `user`, `clicks`, `status`, `sl_id`, `created_at`

### 2. **User (Model)**
- Native Django `User` model.
- Linked via ForeignKey to each `Link`.

### 3. **Views (Logic Functions)**

- `index` – Displays dashboard with user links.
- `index_form` – Handles submission and creation of short links.
- `get_clicks` – Updates click statistics for a link.

### 4. **Helpers (API Calls)**

- `shorten_url_helper` – Calls Rebrandly API to create short URLs.
- `get_clicks_helper` – Retrieves click data from Rebrandly.

### 5. **Templates**

- `index.html` – Main UI for displaying user links and form.
- `base.html` – Base UI theme for all Ziplink pages.

---

## Contexts

### 1. **Users Links limit**

- Simple users have a link creation limit. 
- Authenticated users can create and manage multiple links.

### 2. **Link Creation Behind the Scene**

- Created via form submission.
- Sent to Rebrandly for shortening.
- Stored in local DB with `sl_id`.
- Updated later with click stats from Rebrandly.
- Handle API failures gracefully (timeouts, invalid responses).
- Efficient use of indexing (e.g., `sl_id` or `created_at`) for fast queries.

### 3. **Rebrandly Integration**
- Central to shortening and analytics.
- Requires API key and stable internet.

### 4. **Frontend UX Flow**
- Form → Link shortened → Dashboard refreshes with new link.
- Dashboard shows real-time click counts.

---

