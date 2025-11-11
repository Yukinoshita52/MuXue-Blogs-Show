// // source/js/rewrite-cdn.js

// document.addEventListener('DOMContentLoaded', function() {
//     // 正则表达式匹配 GitHub Raw URL
//     const re = /^https:\/\/raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/([^\/]+)\/([^"'\)\s]+)/;

//     // 1. 查找所有图片（img）标签
//     const images = document.querySelectorAll('img');
    
//     images.forEach(img => {
//         const src = img.getAttribute('src');
//         if (src) {
//             const match = src.match(re);
            
//             if (match) {
//                 const [fullMatch, user, repo, ver, path] = match;
                
//                 // 构建 jsDelivr CDN URL
//                 const cdnUrl = `https://cdn.jsdelivr.net/gh/${user}/${repo}@${ver}/${path}`;
                
//                 // 替换 src 属性
//                 img.setAttribute('src', cdnUrl);
                
//                 // 如果 img 标签有 data-src 属性（懒加载通常使用），也替换掉
//                 const dataSrc = img.getAttribute('data-src');
//                 if (dataSrc && dataSrc === src) {
//                     img.setAttribute('data-src', cdnUrl);
//                 }
//             }
//         }
//     });
    
//     // 2. 查找可能包含 GitHub Raw URL 的其他元素（例如 a 标签的 href，如果需要）
//     // ... 
// });