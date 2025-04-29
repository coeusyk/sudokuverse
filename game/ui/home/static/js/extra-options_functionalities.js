const allColouredStats = Array.from(document.getElementsByClassName("stats-variable"));
const gamesFinished = allColouredStats[1];

const entriesDiv = document.getElementById("entries");
const entries = entriesDiv.getElementsByTagName("div");

const logOutBtn = document.getElementById("log-out-btn");


function logOut() {
    fetch("/home", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({"log-out": true})
    })
        .then(response => response.json())
        .then(data => {
            if (data["success"] === true) {
                window.location.href = "/";  // Redirecting to the main window
            }
        });
}


/**
 * Sends a GET request to the server (Python-Flask) for getting atmost 5 latest completed games
 * and adds those entries to HTML which are unregistered (not added yet)
 */
function getGameInfo() {
    if (parseInt(gamesFinished.innerText) > entries.length) {
        fetch("/home", {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                const entry_ids = Array.from(data["entry-id"]);

                for (let i = 0; i < entry_ids.length; i++) {
                    let entry_validation = validateEntry(entry_ids[i]);

                    if (entry_validation) {
                        let diff = data["difficulty"][i]; let hintsUsed = data["hints-used"][i];
                        let timeTaken = data["time-taken"][i]; let dateTime = data["date-time"][i];

                        addEntry(entry_ids[i], diff, hintsUsed, timeTaken, dateTime);
                    }
                }
            });
    }
}


function changeStatColour() {
    allColouredStats.forEach(stat => {
        if (stat.innerText.includes("None")) {
            stat.classList.remove("stats-variable");
            stat.classList.add("stats-const");
        } 
        
        else {
            stat.classList.add("stats-variable");
            stat.classList.remove("stats-const");
        }
    });
}


function validateEntry(entry_id) {
    for (let entry of entries) {
        if (entry.id === entry_id) {
            return false;
        }
    }

    return true;
}


function addEntry(entry_id, diff, hints, time, dateTime) {
    const entry = document.createElement("div");
    entry.setAttribute('id', entry_id);  // Setting the entry id

    if (entries.length > 0) {
        const entrySeparator = document.createElement("hr");
        entrySeparator.classList.add("entry-separator");

        if (entries.length === 1) {
            const lastEntry = entries[0];
            lastEntry.append(entrySeparator);

            lastEntry.classList.remove("entry_type-1");
            lastEntry.classList.add("entry_type-2");
        } else {
            const lastEntry = entries[entries.length - 1];
            lastEntry.append(entrySeparator);

            lastEntry.classList.remove("entry_type-1");
            lastEntry.classList.add("entry_type-2");
        }
    }

    entry.classList.add("entry", "entry_type-1");

    const firstThreeInfo = [diff, hints, time];

    // For the first three info (diff, hints, time):
    for (let i = 0; i < 3; i++) {
        const cgInfo = document.createElement("span");  // cg -> completed games
        cgInfo.classList.add("c-g-info");
        cgInfo.innerText = firstThreeInfo[i];

        entry.append(cgInfo);
    }

    // For date-time:
    const cgDateTimeInfo = document.createElement("span");
    cgDateTimeInfo.classList.add("c-g-info");
    cgDateTimeInfo.innerText = `${dateTime[0]}\n${dateTime[1]}`;
    
    entry.append(cgDateTimeInfo);

    entriesDiv.appendChild(entry);
}


changeStatColour();  // Initial check
getGameInfo();  // Initial check

logOutBtn.addEventListener("click", logOut);
