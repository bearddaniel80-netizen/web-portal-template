import express from "express";
import cors from "cors";
import { forwardFastapi } from "./middleware/forewardFastapi.js";
import { upload, upload_to_fastapi } from "./utils/fastapi.js";

const app = express();

app.use(express.json());
app.use(cors());

/*
 * ==================================================
 * Dynamic Routes
 * ==================================================
 */
app.get(
  "/services/:application_id/status",
  forwardFastapi(
    (req) => `/api/applications/${encodeURIComponent(req.params.application_id)}/status`
  )
);
app.post(
  "/services/:application_id/start",
  forwardFastapi(
    (req) => `/api/applications/${encodeURIComponent(req.params.application_id)}/start`,
    false
  )
);
app.post(
  "/services/:application_id/stop",
  forwardFastapi(
    (req) => `/api/applications/${encodeURIComponent(req.params.application_id)}/stop`,
    false
  )
);
app.post(
  "/services/:application_id/activate",
  forwardFastapi(
    (req) => `/api/applications/${encodeURIComponent(req.params.application_id)}/activate`,
    false
  )
);
/*
 * ==================================================
 * Static Routes
 * ==================================================
 */

app.listen(4000, "0.0.0.0", () => {
  console.log("Server listening on port 4000");
});