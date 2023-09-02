const filterUsername = (user) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name} ${user.last_name}`;
  } else if (user.username) {
    return user.username;
  } else {
    return user.email;
  }
}

const isAuthenticatedUser = (uid1, uid2) => {
  return uid1 === uid2;
}

export { filterUsername, isAuthenticatedUser };
