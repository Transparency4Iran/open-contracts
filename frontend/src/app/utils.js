export function formatPrice(num) {
  let str1 = num + '';
  const l = str1.length;
  const k = l % 3;
  let ans = '';
  for (let i = l - 1; i >= 0; i--) {
    ans = str1.charAt(i) + ans;
    if ((i - k) % 3 === 0 && i < l - 1 && i > 0) {
      ans = ',' + ans;
    }
  }
  return ans;
};