const HOST: string = window.location.hostname === 'localhost' ? 'http://localhost:8000' : window.location.origin;
export const BASE_URL: string = 'http://localhost';
export const BACKEND_URL: string = HOST + '/api/v1/';
