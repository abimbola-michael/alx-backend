import { createClient, print } from "redis";
const client = createClient();
// Event listener for when the client connects successfully
client.on("connect", () => {
  console.log("Redis client connected to the server");
});

// Event listener for errors
client.on("error", (err) => {
  console.error("Redis client not connected to the server:", err);
});

function createHash() {
  client.hset("HolbertonSchools", "Portland", "50", print);
  client.hset("HolbertonSchools", "Seattle", "80", print);
  client.hset("HolbertonSchools", "New York", "20", print);
  client.hset("HolbertonSchools", "Bogota", "20", print);
  client.hset("HolbertonSchools", "Cali", "40", print);
  client.hset("HolbertonSchools", "Paris", "2", print);
}
function displayHash() {
  client.hgetall("HolbertonSchools", (err, reply) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log(reply);
  });
}
createHash();
displayHash();
