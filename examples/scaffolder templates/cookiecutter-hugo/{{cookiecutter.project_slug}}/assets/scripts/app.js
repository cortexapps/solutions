import add from './add'

const multiply = (first, second) => {
    let result = 0
    for (let counter = 0; counter < second; counter++) {
        result = add(result, first)
    }
    return result
}

export default multiply