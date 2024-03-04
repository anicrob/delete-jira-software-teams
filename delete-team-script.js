var fs = require("fs");
var util = require("util");
var log_file = fs.createWriteStream(__dirname + "/debug.log", { flags: "w" });
var log_stdout = process.stdout;
console.log = function (d) {
  log_file.write(util.format(d) + "\n");
  log_stdout.write(util.format(d) + "\n");
};
const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...args));
require("dotenv").config();
const path = "./Teams.csv";
let index = 100

//function to delete teams
const deleteTeams = async (ids) => {
  try {
    //every 2 seconds, delete a team
    setTimeout(async () => {
      const response = await fetch(
        `${process.env.URL}/gateway/api/public/teams/v1/org/${process.env.ORG_ID}/teams/${ids[index]}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Basic ${process.env.API_KEY}`,
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        //if the response was not ok, show the status
        console.log(`${new Date().toGMTString()} - ${response.status} ${response.statusText} has occured trying to delete team with id ${ids[index]}`) ;
        //increase the index
        index += 1
        //continue deleting the rest of the teams
        deleteTeams(ids);
        return;
      }
      //if the index is less than the last index in the ids array
      if(index < ids.length - 1){
        //add 1 to the index to continue moving through the array
        index += 1
        //call deleteTeams function again
        deleteTeams(ids);
      } else {
        //if there are no more ids left, let the user know the script is done!
        console.log(`${new Date().toGMTString()} - There are no more team ids left. Please check the debug.log file for errors.`)
        return;
      }
      //let the user know that the script has successfully deleted a certain team
      console.log(`${new Date().toGMTString()} - this team has been sucessfully deleted: ${ids[index]}\n`);
    }, 1000);
  } catch (err) {
    console.log(err, index);
  }
};

const getIdsDeleteTeams = async () => {
  // Read the CSV file
  fs.readFile(path, "utf8", async (err, data) => {
    if (err) {
      console.error("Error while reading:", err);
      return;
    }

    // Split the data into lines
    const lines = data.split("\n");

    // Initialize the output array
    const output = [];

    // Loop through each line and split it into fields
    lines.forEach((line) => {
      const fields = line.split(",");
      output.push(fields[0]);
    });

    //remove the "id" header
    const content = output.splice(1);
    
    //send ids to the deleteTeams function to delete
    deleteTeams(content);
  });
};

getIdsDeleteTeams();