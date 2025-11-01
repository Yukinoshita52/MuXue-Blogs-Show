/*!
 * pictureCDN.js — 运行期将 raw.githubusercontent.com 链接替换为 jsDelivr 加速链接
 */
(function () {
  // 将 GitHub raw 链接格式化为 jsDelivr 加速地址
  function toJsDelivr(url) {
    return url.replace(
      /^https?:\/\/raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/main\/(.+)$/i,
      function (_, user, repo, path) {
        return 'https://cdn.jsdelivr.net/gh/' + user + '/' + repo + '/' + path;
      }
    );
  }

  // 遍历所有 <img>，替换 src
  function cdnifyImages() {
    document.querySelectorAll('img').forEach(function (img) {
      var src = img.getAttribute('src') || '';
      if (/^https?:\/\/raw\.githubusercontent\.com\//i.test(src)) {
        img.setAttribute('src', toJsDelivr(src));
      }
    });
  }

  // DOM 就绪后执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', cdnifyImages);
  } else {
    cdnifyImages();
  }
})();
