import axios from 'axios';

export const login = user => {
  return axios
    .post('http://127.0.0.1:5000/login', {
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
    if(sessionStorage.getItem('usertoken') == null){
      return false
    }
    return true
}