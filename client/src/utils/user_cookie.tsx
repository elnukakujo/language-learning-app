'use server'

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function setUserCookie(userId: string) {
  const cookieStore = await cookies()
  cookieStore.set('selected_user_id', userId, {
    httpOnly: true,
    path: '/',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 365, // 1 year
  })
  redirect('/')
}

export async function clearUserCookie() {
  const cookieStore = await cookies()
  cookieStore.delete('selected_user_id')
  redirect('/')
}

export async function getCurrentUserId(): Promise<string | null> {
  const cookieStore = await cookies()
  return cookieStore.get('selected_user_id')?.value ?? null
}