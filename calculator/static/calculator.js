
const calculator = document.querySelector('.calculator') //select div class
const keys = calculator.querySelector('.calculator-keys') //within calculator div select other div
const display = document.querySelector('.calculator-display')


const getKeyType = (key) => {
  const { action } = key.dataset
  if (!action) return 'number'
  if (
    action === 'add' ||
    action === 'subtract' ||
    action === 'multiply' ||
    action === 'divide'
  ) return 'operator'
  return action
}


const createResultString = (key, displayedNum, state) => {
  const keyContent = key.textContent
  const action = key.dataset.action
  const firstValue = state.firstValue
  const modValue = state.modValue
  const operator = state.operator
  const previousKeyType = state.previousKeyType
  const keyType = getKeyType(key)

  if (keyType === 'number'){
    if (
      displayedNum === '0' ||
      previousKeyType === 'operator' ||
      previousKeyType === 'calculate'
    ){
      return keyContent
    }else{
      return displayedNum + keyContent
    }
  }

  if (keyType === 'decimal'){
    if (!displayedNum.includes('.')){
      return displayedNum + '.'
    }
    if (previousKeyType === 'operator' || previousKeyType === 'calculate'){
      return '0.'
    }
    return displayedNum
  }

  if (keyType === 'operator'){
    const firstValue = calculator.dataset.firstValue
    const operator = calculator.dataset.operator

    if (
      firstValue &&
      operator &&
      previousKeyType !== 'operator' &&
      previousKeyType !== 'calculate'
    ){
      return calculate(firstValue, operator, displayedNum)
    }else{
      return displayedNum
    }
  }

  if (keyType === 'clear') return 0

  if (keyType === 'calculate'){
    let firstValue = calculator.dataset.firstValue
    const operator = calculator.dataset.operator
    let secondValue = displayedNum

    if (firstValue) {
      if (previousKeyType === 'calculate'){
        firstValue = displayedNum
        secondValue = calculator.dataset.modValue
      }
      return calculate(firstValue, operator, secondValue)
    }else {
      return displayedNum
    }
  }

}


const updateVisualState = (key, calculator) => {
  const keyType = getKeyType(key)
  Array.from(key.parentNode.children).forEach(k => k.classList.remove('is-depressed'))

  if (keyType === 'operator') key.classList.add('is-depressed')

  if (keyType === 'clear' && key.textContent !== 'AC'){
    key.textContent = 'AC'
  }

  if (keyType !== 'clear'){
    const clearButton = calculator.querySelector('[data-action=clear]')
    clearButton.textContent = 'CE'
  }
}


const updateCalculatorState = (key, calculator, calcValue, displayedNum) => {
  const keyType = getKeyType(key)
  const previousKeyType = calculator.dataset.previousKeyType
  calculator.dataset.previousKeyType = keyType
  let firstValue = calculator.dataset.firstValue
  let operator = calculator.dataset.operator
  let {action} = key.dataset

  if (keyType === 'operator'){
    if (
      firstValue &&
      operator &&
      previousKeyType !== 'operator' &&
      previousKeyType !== 'calculate'
    ){
      calculator.dataset.firstValue = calcValue
    }else {
      calculator.dataset.firstValue = displayedNum
    }

    calculator.dataset.operator = action
  }

  if (keyType === 'clear'){
    if (key.textContent === 'AC') {
      calculator.dataset.firstValue = ''
      calculator.dataset.modValue = ''
      calculator.dataset.operator = ''
      calculator.dataset.previousKeyType = ''
    }
    display.textContent = 0
    calculator.dataset.previousKeyType = 'clear'
  }

  if (keyType === 'calculate'){
    let secondValue = displayedNum

    if (firstValue) {
      if (previousKeyType === 'calculate'){
        console.log('double equals')
        console.log(secondValue)
        secondValue = calculator.dataset.modValue
        console.log(secondValue)
      }
    }
    calculator.dataset.modValue = secondValue
  }

}


keys.addEventListener('click', e => {

  if (e.target.matches('button')){

    const key = e.target
    const displayedNum = display.textContent

    const resultString = createResultString(key, displayedNum, calculator.dataset)

    display.textContent = resultString
    updateCalculatorState(key, calculator, resultString, displayedNum)
    updateVisualState(key, calculator)
  }
  })


const calculate = (n1, operator, n2) => {
  const firstNum = parseFloat(n1)
  const secondNum = parseFloat(n2)
  if (operator === 'add'){
    return firstNum + secondNum
  }
  if (operator === 'subtract'){
    return firstNum - secondNum
  }
  if (operator === 'multiply'){
    return firstNum * secondNum
  }
  if (operator === 'divide'){
    return firstNum / secondNum
  }
}
