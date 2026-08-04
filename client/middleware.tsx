import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // ── 1. User cookie check ──────────────────────────
  const userId = request.cookies.get('selected_user_id')?.value
  if (pathname !== '/' && !userId) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  // ── 2. Language cookie check (example) ───────────
  const langId = request.cookies.get('selected_language_id')?.value
  if (pathname.startsWith('/lessons') && !langId) {
    return NextResponse.redirect(new URL('/languages', request.url))
  }

  // ── 3. Add headers, logging, etc. ─────────────────
  const response = NextResponse.next()
  response.headers.set('x-user-id', userId ?? '')
  return response
}