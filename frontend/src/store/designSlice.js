import { createSlice } from '@reduxjs/toolkit';

export const designSlice = createSlice({
    name: 'design',
    initialState:{
        allDesigns: [],
        designInfo: {},
    },
    reducers:{
        addDesign:(state, payload) => {
            state.allDesigns.push(payload);
        },
        deleteDesign:(state) =>{

        },
        setCurDesign:(state) => {

        },
    }
})

export const { addDesign, deleteDesign, setCurDesign } = designSlice.actions;
export default designSlice.reducer;