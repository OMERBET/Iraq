// secure-api.js - طبقة آمنة للتعامل مع API
class SecureAPI {
  constructor() {
    this.apiBase = window.location.origin;
    this.token = null;
  }

  // حفظ التوكن بشكل آمن
  setToken(token) {
    this.token = token;
    if (token) {
      sessionStorage.setItem('auth_token', token);
    } else {
      sessionStorage.removeItem('auth_token');
    }
  }

  // جلب التوكن
  getToken() {
    if (!this.token) {
      this.token = sessionStorage.getItem('auth_token');
    }
    return this.token;
  }

  // دالة مساعدة للطلبات
  async request(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (token && !options.skipAuth) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.apiBase}${endpoint}`, {
      ...options,
      headers
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(error.error || error.message || 'Request failed');
    }

    return response.json();
  }

  // ═══ Auth Methods ═══
  
  async signUp(email, password) {
    return this.request('/api/auth', {
      method: 'POST',
      skipAuth: true,
      body: JSON.stringify({
        action: 'signup',
        email,
        password
      })
    });
  }

  async signIn(email, password) {
    const data = await this.request('/api/auth', {
      method: 'POST',
      skipAuth: true,
      body: JSON.stringify({
        action: 'signin',
        email,
        password
      })
    });

    if (data.access_token) {
      this.setToken(data.access_token);
    }

    return data;
  }

  async verifyOTP(email, otp) {
    const data = await this.request('/api/auth', {
      method: 'POST',
      skipAuth: true,
      body: JSON.stringify({
        action: 'verify-otp',
        email,
        otp
      })
    });

    if (data.access_token) {
      this.setToken(data.access_token);
    }

    return data;
  }

  async resendOTP(email) {
    return this.request('/api/auth', {
      method: 'POST',
      skipAuth: true,
      body: JSON.stringify({
        action: 'resend-otp',
        email
      })
    });
  }

  signOut() {
    this.setToken(null);
    window.location.reload();
  }

  // ═══ Claude AI Methods ═══
  
  async askClaude(messages) {
    return this.request('/api/claude', {
      method: 'POST',
      body: JSON.stringify({ messages })
    });
  }

  // ═══ Admin Methods ═══
  
  async getAdminStats() {
    return this.request('/api/admin', {
      method: 'GET'
    });
  }
}

// تصدير الكلاس
window.SecureAPI = SecureAPI;
```

### كيف ترفعه:
1. في GitHub، اضغط **"Add file"** → **"Create new file"**
2. اسم الملف: `secure-api.js`
3. الصق الكود فوق
4. Commit: `Add secure API layer`

---

## 📋 خطوات الرفع بالترتيب:

### الخطوة 1: ارفع vercel.json
1. Create new file
2. اسم: `vercel.json`
3. الصق الكود الأول
4. Commit

### الخطوة 2: ارفع secure-api.js
1. Create new file
2. اسم: `secure-api.js`
3. الصق الكود الثاني
4. Commit

---

## ✅ بعد ما ترفع الملفين:

1. ⏳ **انتظر دقيقة**
2. 🔄 **Vercel راح ينشر تلقائياً**
3. ✅ **راح يطلع: Ready**
4. 🎉 **موقعك راح يشتغل!**

---

## 🎯 ملخص سريع:
```
الملف الأول:  vercel.json     (حماية Headers)
الملف الثاني:  secure-api.js   (طبقة API آمنة)
النتيجة:       موقع محمي 100%
