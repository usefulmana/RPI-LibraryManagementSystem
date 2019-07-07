current_datetime = new Date();
let formatted_date =
  current_datetime.getFullYear() +
  ':' +
  (current_datetime.getMonth() + 1) +
  ':' +
  current_datetime.getDate();
console.log(formatted_date);
