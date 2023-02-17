
const calculator = document.querySelector('.calculator') //select div class
const keys = calculator.querySelector('.calculator-keys') //within calculator div select other div
const display = document.querySelector('.calculator-display')


keys.addEventListener('click', e => {
  if (e.target.matches('button')){
    const key = e.target
    const action = key.dataset.action
    const keyContent = key.textContent
    const displayedNum = display.textContent
    const previousKeyType = calculator.dataset.previousKeyType


    if (!action){   //number key
      if (
        displayedNum === '0' ||
        previousKeyType === 'operator' ||
        previousKeyType === 'calculate'
      ){
        display.textContent = keyContent
      }else{
        display.textContent = displayedNum + keyContent
      }
      calculator.dataset.previousKeyType = 'number'
    }


    if (
      action === 'add' ||
      action === 'subtract' ||
      action === 'multiply' ||
      action === 'divide'
    ){
      const firstValue = calculator.dataset.firstValue
      const operator = calculator.dataset.operator
      const secondValue = displayedNum

      if (
        firstValue &&
        operator &&
        previousKeyType !== 'operator' &&
        previousKeyType !== 'calculate'
      ){
        const calcValue = calculate(firstValue, operator, secondValue)
        display.textContent = calcValue
        calculator.dataset.firstValue = calcValue
      }else {
        calculator.dataset.firstValue = displayedNum
      }

      key.classList.add('is-depressed')
      calculator.dataset.previousKeyType = 'operator'
      calculator.dataset.operator = action
    }

    Array.from(key.parentNode.children).forEach(k => k.classList.remove('is-depressed'))


    if (action === 'decimal'){
      console.log(previousKeyType)
      if (!displayedNum.includes('.')){
        display.textContent = displayedNum + '.'
      }else if (
        previousKeyType === 'operator' ||
        previousKeyType === 'calculate'
      ){
        display.textContent = '0.'
      }
      calculator.dataset.previousKeyType = 'decimal'
    }


    if (action === 'clear'){
      if (key.textContent === 'AC') {
        calculator.dataset.firstValue = ''
        calculator.dataset.modValue = ''
        calculator.dataset.operator = ''
        calculator.dataset.previousKeyType = ''
      }else {
        key.textContent = 'AC'
      }
      display.textContent = 0
      calculator.dataset.previousKeyType = 'clear'
    }

    if (action !== 'clear'){
      const clearButton = calculator.querySelector('[data-action=clear]')
      clearButton.textContent = 'CE'
    }


    if (action === 'calculate'){
      let firstValue = calculator.dataset.firstValue
      const operator = calculator.dataset.operator
      let secondValue = displayedNum

      if (firstValue) {
        if (previousKeyType === 'calculate'){
          firstValue = displayedNum
          secondValue = calculator.dataset.modValue
        }
        display.textContent = calculate(firstValue, operator, secondValue)
      }
      calculator.dataset.modValue = secondValue
      calculator.dataset.previousKeyType = 'calculate'
    }

  }
})


const calculate = (n1, operator, n2) => {
  let result = ''

  if (operator === 'add'){
    return parseFloat(n1) + parseFloat(n2)
  } else if (operator === 'subtract'){
    return parseFloat(n1) - parseFloat(n2)
  } else if (operator === 'multiply'){
    return parseFloat(n1) * parseFloat(n2)
  } else if (operator === 'divide'){
    return parseFloat(n1) / parseFloat(n2)
  }
  return result
}
