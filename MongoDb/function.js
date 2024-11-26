db.system.js.save({
    _id: "addUser",
    value: function (firstName, lastName, age, email) {
        return db.users.insertOne({
            first_name: firstName,
            sure_name: lastName,
            age: age,
            email: email,
            isActive: true
        });
    }
});