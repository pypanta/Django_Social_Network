const createdBy = (user) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name} ${user.last_name}`;
  } else if (user.username) {
    return user.username;
  } else {
    return user.email;
  }
}

export default createdBy;
