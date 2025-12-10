// cec/deno_api/main.ts
import { serve } from "https://deno.land/std@0.140.0/http/server.ts";

console.log("Deno HTML fetcher API starting...");

serve(async (req) => {
  const url = new URL(req.url);
  if (url.pathname === "/fetch") {
    const targetUrl = url.searchParams.get("url");
    const userAgent = Deno.env.get("USER_AGENT"); // Read from environment variable
    if (!targetUrl) {
      return new Response("Missing 'url' query parameter", { status: 400 });
    }
    try {
      console.log(`Fetching ${targetUrl}`);
      const headers = new Headers();
      if (userAgent) {
        headers.set("User-Agent", userAgent);
      }
      const resp = await fetch(targetUrl, { headers: headers });
      // Ensure the response is ok before proceeding
      if (!resp.ok) {
        throw new Error(`Failed to fetch: ${resp.status} ${resp.statusText}`);
      }
      const source = await resp.text();
      return new Response(source, { headers: { "Content-Type": "text/html" } });
    } catch (e) {
        console.error(`Error fetching URL: ${targetUrl}`, e);
        return new Response(e.message, { status: 500 });
    }
  } else if (url.pathname === "/health") {
    return new Response("OK", { status: 200 });
  }
  return new Response("Not Found", { status: 404 });
}, { port: 8000 });

console.log("Deno HTML fetcher API running on http://localhost:8000");
