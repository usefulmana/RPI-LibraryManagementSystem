import axios from 'axios';
import { LOG_IN } from './rest_api_routes';

export const login = user => {
  return axios
    .post(LOG_IN, {
      username: user.username,
      password: user.password
    })
    .then(response => {
      sessionStorage.setItem('usertoken', response.data);
      return response.data;
    })
    .catch(err => {
      console.log(err);
    });
};

export const isAuthenticated = () => {
  if (sessionStorage.getItem('usertoken') == null) {
    return false;
  } else {
    return true;
  }
};
