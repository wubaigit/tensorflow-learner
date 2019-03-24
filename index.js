function sum(...args) {
  Function.prototype.value = () => {
    delete Function.prototype.value;
    return args.reduce((a, b) => a + b);
  }
  return function (...arg) {
    return sum(...arg, ...args);
  }
}

const a = sum(1)(2, 3)(4).value();

const b = sum(1)(2).value();

function name(a, b) {
  return function() {
    return a + b;
  }
}

const c = name(1, 3);

console.log(a, b, c);
