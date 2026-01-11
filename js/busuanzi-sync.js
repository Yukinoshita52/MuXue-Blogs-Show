(function() {
    const targetHost = 'busuanzi.ibruce.info';

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                // 匹配动态插入的 script 标签
                if (node.tagName === 'SCRIPT' && node.src && node.src.includes(targetHost)) {
                    // 1. 立即停止当前阻塞加载
                    node.type = 'text/javascript-intercepted'; 
                    const originalSrc = node.src;
                    node.remove(); 

                    // 2. 构造异步请求
                    const asyncScript = document.createElement('script');
                    asyncScript.src = originalSrc;
                    asyncScript.async = true; // 强制异步
                    asyncScript.defer = true;
                    
                    // 3. 静默处理 502 错误
                    asyncScript.onerror = () => {
                        console.warn('Busuanzi request failed (502). Blocking UI artifacts.');
                        document.querySelectorAll('[id^="busuanzi_container_"]').forEach(el => {
                            el.style.display = 'none';
                        });
                    };

                    document.head.appendChild(asyncScript);
                    console.log('Busuanzi request intercepted and converted to async:', originalSrc);
                }
            });
        });
    });

    // 监听整个文档的节点变化
    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });
})();