(function() {
    // 1. 强制视觉静默
    const style = document.createElement('style');
    style.innerHTML = '[id^="busuanzi_container_"] { display: none !important; }';
    document.documentElement.appendChild(style);

    // 2. 劫持 appendChild (核心：不蒜子 fetch 方法的出口)
    const originalAppendChild = Element.prototype.appendChild;
    Element.prototype.appendChild = function(node) {
        if (node && node.tagName === 'SCRIPT' && node.src && node.src.includes('busuanzi.ibruce.info/busuanzi?')) {
            // 强制转换属性
            node.async = true;
            node.defer = false; // 撤销阻塞执行队列的 defer
            
            // 注入硬超时断路器
            const abortTimeout = setTimeout(() => {
                console.warn('Busuanzi 502/Timeout: Terminating hang request.');
                node.src = ''; 
                node.remove();
            }, 3000); // 3秒不响应即物理断开

            node.onload = node.onerror = () => clearTimeout(abortTimeout);
            
            console.log('Busuanzi appendChild intercepted.');
        }
        return originalAppendChild.apply(this, arguments);
    };

    // 3. 补充拦截 insertBefore (不蒜子其他版本的备选出口)
    const originalInsertBefore = Node.prototype.insertBefore;
    Node.prototype.insertBefore = function(newNode, referenceNode) {
        if (newNode && newNode.tagName === 'SCRIPT' && newNode.src && newNode.src.includes('busuanzi.ibruce.info/busuanzi?')) {
            newNode.async = true;
            newNode.defer = false;
        }
        return originalInsertBefore.apply(this, arguments);
    };
})();