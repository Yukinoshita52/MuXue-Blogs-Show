(function() {
    // 1. 拦截所有脚本插入行为
    const originalInsertBefore = Node.prototype.insertBefore;
    Node.prototype.insertBefore = function(newNode, referenceNode) {
        if (newNode && newNode.tagName === 'SCRIPT' && newNode.src) {
            const url = newNode.src;
            
            // 匹配阻塞的动态数据接口
            if (url.includes('busuanzi.ibruce.info/busuanzi?')) {
                console.log('Detected blocking data request, converting to async...');
                newNode.async = true;
                
                // 强制设置超时处理：如果 5 秒没响应，直接视为失败
                const timeout = setTimeout(() => {
                    newNode.onerror();
                }, 5000);

                newNode.onload = newNode.onerror = function() {
                    clearTimeout(timeout);
                    // 如果失败，清理占位符
                    if (!window[url.split('jsonpCallback=')[1]]) {
                        document.querySelectorAll('[id^="busuanzi_container_"]').forEach(el => el.remove());
                    }
                };
            }
        }
        return originalInsertBefore.apply(this, arguments);
    };

    // 2. CSS 预处理：默认隐藏所有计数区域
    const style = document.createElement('style');
    style.innerHTML = '[id^="busuanzi_container_"] { display: none !important; }';
    document.documentElement.appendChild(style);
})();