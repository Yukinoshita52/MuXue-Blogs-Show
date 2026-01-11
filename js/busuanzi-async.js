(function() {
    // 1. 立即设置一个全局占位函数，防止不蒜子脚本加载后找不到回调导致报错
    const bszCallbackName = 'BusuanziCallback_' + Math.floor(Math.random() * 1000000000000);
    window[bszCallbackName] = function(data) {
        try {
            if (data.site_pv) document.getElementById('busuanzi_value_site_pv').innerHTML = data.site_pv;
            if (data.site_uv) document.getElementById('busuanzi_value_site_uv').innerHTML = data.site_uv;
            if (data.page_pv) document.getElementById('busuanzi_value_page_pv').innerHTML = data.page_pv;
            
            ['site_pv', 'site_uv', 'page_pv'].forEach(id => {
                const el = document.getElementById(`busuanzi_container_${id}`);
                if (el) el.style.display = 'inline';
            });
        } catch (e) {}
    };

    // 2. 拦截 document.createElement，将所有不蒜子请求强制转为异步
    const originalCreateElement = document.createElement;
    document.createElement = function(tagName) {
        const el = originalCreateElement.apply(this, arguments);
        if (tagName.toLowerCase() === 'script') {
            const descriptor = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src');
            Object.defineProperty(el, 'src', {
                set: function(value) {
                    if (value.includes('busuanzi.ibruce.info')) {
                        this.async = true; // 强制异步
                        this.defer = true;
                        // 针对 502 错误监听
                        this.onerror = function() {
                            console.warn('Busuanzi 502 detected. Silencing...');
                            document.querySelectorAll('[id^="busuanzi_container_"]').forEach(c => c.style.display = 'none');
                        };
                    }
                    descriptor.set.call(this, value);
                },
                get: function() {
                    return descriptor.get.call(this);
                }
            });
        }
        return el;
    };

    // 3. 处理 CSS，防止 502 时页面显示源代码占位符
    const style = document.createElement('style');
    style.innerHTML = '[id^="busuanzi_container_"] { display: none; }';
    document.head.appendChild(style);
})();