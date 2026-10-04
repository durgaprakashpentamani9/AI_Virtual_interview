import {create} from 'zustand';
export const useInterview=create((set)=>({question:null,feedback:null,recording:false,online:navigator.onLine,muted:false,set:(x)=>set(x)}));
