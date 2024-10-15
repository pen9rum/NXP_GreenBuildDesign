import { configureStore } from '@reduxjs/toolkit';
import { designSlice } from './designSlice';

export const store = configureStore({
  reducer: {
    designController: designSlice,
  },
});
