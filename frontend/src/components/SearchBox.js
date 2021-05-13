import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'

function SearchBox() {

    // keyword will store the value that is searched
    const [keyword, setKeyword] = useState('')

    // to get access to the history prop
    let history = useHistory()

    const submitHandler = (e) => {
        e.preventDefault()
        if (keyword) {
            // just sending the user to the homepage with the keyword appende
            history.push(`/?keyword=${keyword}`)
        } else {
            // sending the user to the original page
            history.push(history.push(history.location.pathname))
        }
    }
    return (
        <Form onSubmit={submitHandler} inline >
            <Form.Control
                type='text'
                name='q'
                onChange={(e) => setKeyword(e.target.value)}
                className='mr-sm-2 ml-sm-5'>
            </Form.Control>
            <Button
                type='submit'
                variant='outline-success'
                className='p-2'>
                Seacrh
            </Button>
        </Form >
    )
}

export default SearchBox
