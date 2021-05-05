import {
    CART_ADD_ITEM,
    CART_REMOVE_ITEM
} from '../constants/cartConstants'

//it'll just be the all the items in the cart
export const cartReducer = (state = { cartItems: [] }, action) => {
    switch (action.type) {
        case CART_ADD_ITEM:
            const item = action.payload
            const existsItem = state.cartItems.find(x => x.product === item.product)

            if (existsItem) {
                return {
                    ...state,
                    cartItems: state.cartItems.map(x => x.product === existsItem.product ? item : x)
                }
            } else {
                return {
                    ...state,
                    cartItems: [...state.cartItems, item]
                }
            }

        case CART_REMOVE_ITEM:
            return {
                // spread operator
                ...state,
                // this will filter out the product which you want to delete from the cart
                cartItems: state.cartItems.filter(x => x.product !== action.payload)
            }


        default:
            return state

    }
}


