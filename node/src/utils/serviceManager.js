import { readFileSync } from "fs";

function readSecret(name) {
  const path = `/run/secrets/${name}`;

  try {
    return readFileSync(path, "utf8").trim();
  } catch (err) {
    console.error(`Could not read secret: ${path}`);
    process.exit(1);
  }
}

const SERVICE_MANAGER_URL = process.env.SERVICE_MANAGER_URL;
const SERVICE_MANAGER_API_KEY = readSecret("service_manager_api_key");

export async function get_service_manager(
  path,
  {
    body,
    headers = {},
  } = {}
) {
  const response = await fetch(
    `${SERVICE_MANAGER_URL}${path}`,
    {
      method: "GET",

      headers: {
        "X-Internal-Key": SERVICE_MANAGER_API_KEY,
        "Accept": "application/json",

        ...(body !== undefined
          ? {
              "Content-Type": "application/json",
            }
          : {}),

        ...headers,
      },

      ...(body !== undefined
        ? {
            body: JSON.stringify(body),
          }
        : {}),
    }
  );

  return parseResponse(response);
}

export async function post_service_manager(
  path,
  {
    body,
    headers = {},
  } = {}
) {
  const response = await fetch(
    `${SERVICE_MANAGER_URL}${path}`,
    {
      method: "POST",

      headers: {
        "X-Internal-Key": SERVICE_MANAGER_API_KEY,
        "Accept": "application/json",

        ...(body !== undefined
          ? {
              "Content-Type": "application/json",
            }
          : {}),

        ...headers,
      },

      ...(body !== undefined
        ? {
            body: JSON.stringify(body),
          }
        : {}),
    }
  );

  return parseResponse(response);
}