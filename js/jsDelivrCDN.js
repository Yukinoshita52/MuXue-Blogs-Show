/* scripts/rewrite-cdn.js */
hexo.extend.filter.register('before_post_render', function (data) {
  // 匹配：https://raw.githubusercontent.com/<user>/<repo>/<version>/<path>
  const re = /https:\/\/raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/([^\/]+)\/([^\)\s'"]+)/g;
  data.content = data.content.replace(re, (m, user, repo, ver, path) => {
    // 为生产更稳健，可在此把 ver 改为某个提交哈希或标签
    return `https://cdn.jsdelivr.net/gh/${user}/${repo}@${ver}/${path}`;
  });
  return data;
});