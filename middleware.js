// middleware.js - حماية متقدمة باستخدام Vercel Edge Functions
import { NextResponse } from 'next/server';

// خريطة بسيطة لتتبع الطلبات (في الإنتاج، استخدم Vercel KV أو Redis)
const requestCounts = new Map();

// تنظيف الخريطة كل دقيقة
setInterval(() => {
  const now = Date.now();
  for (const [key, data] of requestCounts.entries()) {
    if (now - data.timestamp > 60000) {
      requestCounts.delete(key);
    }
  }
}, 60000);

export function middleware(request) {
  const response = NextResponse.next();
  
  // 1. Security Headers (إضافية)
  response.headers.set('X-DNS-Prefetch-Control', 'on');
  response.headers.set('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');
  
  // 2. Rate Limiting
  const ip = request.ip || request.headers.get('x-forwarded-for') || 'unknown';
  const path = request.nextUrl.pathname;
  
  // تطبيق Rate Limiting على API endpoints فقط
  if (path.startsWith('/api/')) {
    const key = `${ip}:${path}`;
    const now = Date.now();
    const limit = path.includes('/auth') ? 10 : 30; // 10 طلبات للتوثيق، 30 للباقي
    
    if (requestCounts.has(key)) {
      const data = requestCounts.get(key);
      
      if (now - data.timestamp < 60000) {
        // نفس الدقيقة
        if (data.count >= limit) {
          return new NextResponse(
            JSON.stringify({ 
              error: 'Too many requests',
              message: 'يرجى الانتظار قبل المحاولة مرة أخرى',
              retryAfter: Math.ceil((60000 - (now - data.timestamp)) / 1000)
            }),
            { 
              status: 429,
              headers: {
                'Content-Type': 'application/json',
                'Retry-After': String(Math.ceil((60000 - (now - data.timestamp)) / 1000))
              }
            }
          );
        }
        data.count++;
      } else {
        // دقيقة جديدة
        requestCounts.set(key, { count: 1, timestamp: now });
      }
    } else {
      requestCounts.set(key, { count: 1, timestamp: now });
    }
  }
  
  // 3. حظر User Agents المشبوهة
  const userAgent = request.headers.get('user-agent') || '';
  const suspiciousPatterns = [
    /bot/i,
    /crawler/i,
    /spider/i,
    /scraper/i
  ];
  
  const isSuspicious = suspiciousPatterns.some(pattern => pattern.test(userAgent));
  
  if (isSuspicious && path.startsWith('/api/')) {
    // يمكنك السماح لبعض البوتات الشرعية
    const allowedBots = ['googlebot', 'bingbot'];
    const isAllowed = allowedBots.some(bot => userAgent.toLowerCase().includes(bot));
    
    if (!isAllowed) {
      return new NextResponse(
        JSON.stringify({ 
          error: 'Access denied',
          message: 'Suspicious user agent detected'
        }),
        { 
          status: 403,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
  }
  
  // 4. حماية من CSRF (للطلبات التي تغيّر البيانات)
  if (request.method !== 'GET' && request.method !== 'HEAD' && request.method !== 'OPTIONS') {
    const origin = request.headers.get('origin');
    const host = request.headers.get('host');
    
    // تحقق من أن الطلب قادم من نفس النطاق
    if (origin && !origin.includes(host)) {
      return new NextResponse(
        JSON.stringify({ 
          error: 'CSRF protection',
          message: 'Invalid origin'
        }),
        { 
          status: 403,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
  }
  
  return response;
}

// تحديد المسارات التي سيعمل عليها الـ Middleware
export const config = {
  matcher: [
    '/api/:path*',
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
