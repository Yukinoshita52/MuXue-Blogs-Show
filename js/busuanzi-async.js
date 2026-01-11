(function() {
    // 1. 立即注入样式，确保 502 时页面视觉干净
    const style = document.createElement('style');
    style.innerHTML = '[id^="busuanzi_container_"] { display: none !important; }';
    document.documentElement.appendChild(style);

    // 2. 劫持 createElement，修改属性
    const originalCreateElement = document.createElement;
    document.createElement = function(tag) {
        const el = originalCreateElement.apply(this, arguments);
        if (tag.toLowerCase() === 'script') {
            const descriptor = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src');
            Object.defineProperty(el, 'src', {
                set: function(value) {
                    if (value.includes('busuanzi.ibruce.info/busuanzi?')) {
                        // 强制将 defer 转为 async，解除执行队列锁定
                        this.async = true;
                        this.defer = false;
                        this.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
                        
                        // 注入超时机制，防止接口挂起 2 分钟
                        const timeout = setTimeout(() => {
                            console.warn('Busuanzi Timeout - Terminating request.');
                            this.src = ''; // 终止请求
                            this.remove();
                        }, 3000); // 3秒超时

                        this.onload = this.onerror = () => clearTimeout(timeout);
                    }
                    descriptor.set.call(this, value);
                },
                get: function() { return descriptor.get.call(this); }
            });
        }
        return el;
    };
})();