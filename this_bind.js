/**
 * 默认绑定
 */

console.log(this === module.exports); // true

function foo() {
  console.log(this === global); // true
}

foo();

