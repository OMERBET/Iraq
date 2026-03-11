// Middleware temporarily disabled
// The security is handled by:
// - vercel.json (Security Headers)
// - api/auth.js (Authentication protection)
// - api/claude.js (AI API protection)
// - api/admin.js (Admin panel protection)

// Empty matcher = middleware won't run
export const config = {
  matcher: []
};

// Empty handler
export function middleware(request) {
  // Do nothing - pass through
}
