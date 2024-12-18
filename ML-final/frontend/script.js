const students = [
    "180103001", "200107065", "220101097", "220103070", "220103348", "220107003", "220107005", "220107007", "220107008", "220107010", "220107012", "220107014", "220107020", "220107021", "220107027", "220107028", "220107032", "220107037", "220107038", "220107043", "220107048", "220107049", "220107051", "220107052", "220107056", "220107064", "220107065", "220107068", "220107072", "220107075", "220107077", "220107088", "220107092", "220107093", "220107094", "220107097", "220107103", "220107104", "220107108", "220107114", "220107116", "220107118", "220107122", "220107125", "220107127", "220107129", "220107135", "220107139", "220107142", "220107145", "220107148", "220107149", "220107151", "220107152", "220107157", "220107158", "220302069", "220302131", "230302228", "240218005"
    ];
            const dates = ["2024-12-01 9:00", "2024-12-02 9:00", "2024-12-03 9:00", "2024-12-04 9:00", "2024-12-05 9:00", "2024-12-06 9:00", "2024-12-07 9:00", "2024-12-08 9:00", "2024-12-09 9:00", "2024-12-10 9:00", "2024-12-11 9:00", "2024-12-12 9:00", "2024-12-01 9:00", "2024-12-02 9:00", "2024-12-03 9:00", "2024-12-01 9:00", "2024-12-02 9:00", "2024-12-03 9:00", "2024-12-01 9:00", "2024-12-02 9:00", "2024-12-03 9:00", "2024-12-01 9:00", "2024-12-02 9:00", "2024-12-03 9:00", "2024-12-01 9:00", "2024-12-02 9:00", "2024-12-03"];
    
            let lockedCells = new Set();
    
            function showAttendance(subject,dates,students) {
                const attendanceDiv = document.getElementById('attendance');
                attendanceDiv.innerHTML = `
                    <h3>${subject} Attendance</h3>
                    <div class="table-container">
                        <table id="attendance-table">
                            <thead>
                                <tr>
                                    <th>Student ID</th>
                                    ${dates.map(date => `<th>${date}<br><input type="checkbox" class="column-checkbox" data-date="${date}" /></th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${students.map(student => `
                                    <tr>
                                        <td>${student}</td>
                                        ${dates.map((date, index) => `<td data-student="${student}" data-date="${date}" class="attendance-cell"></td>`).join('')}
                                    </tr>`).join('')}
                            </tbody>
                        </table>
                    </div>
                    <div class="btn-container">
                        <button class="set-attendance-btn" onclick="submitAttendance()">Submit Attendance</button>
                        <button id="change" class="set-attendance-btn" onclick="change()">Change Attendance</button>
                        <button class="set-attendance-btn" id="submit-btn" onclick="openPopup()">Photo/Video attendance</button>
                    </div>`;
    
                setupCheckboxListeners();
                setupCellListeners();
            }
    
            function setupCheckboxListeners() {
                const columnCheckboxes = document.querySelectorAll('.column-checkbox');
                columnCheckboxes.forEach((checkbox, colIndex) => {
                    checkbox.addEventListener('change', () => {
                        const table = document.getElementById('attendance-table');
                        const rows = table.querySelectorAll('tbody tr');
    
                        rows.forEach((row) => {
                            const cell = row.children[colIndex + 1];
                            if (lockedCells.has(cell)) return;
                            if (checkbox.checked) {
                                cell.textContent = '✔';
                                cell.classList.remove('red-cross');
                                cell.classList.remove('blue-reason');
                                cell.classList.add('green-check');
                            } else {
                                cell.textContent = 'p';
                                cell.classList.remove('green-check');
                                cell.classList.add('blue-reason');
                            }
                        });
                    });
                });
            }
    
            function setupCellListeners() {
                const cells = document.querySelectorAll('.attendance-cell');
                cells.forEach(cell => {
                    cell.addEventListener('click', () => {
                        if (lockedCells.has(cell)) return;
    
                        if (cell.textContent === '✔') {
                            cell.textContent = '✘';
                            cell.classList.remove('green-check');
                            cell.classList.add('red-cross');
                        } else if (cell.textContent === '✘') {
                            cell.textContent = 'p';
                            cell.classList.remove('red-cross');
                            cell.classList.add('blue-reason');
                        } else if (cell.textContent === 'p') {
                            cell.textContent = '✔';
                            cell.classList.remove('blue-reason');
                            cell.classList.add('green-check');
                        } else {
                            cell.textContent = null;
                            cell.classList.remove('green-check', 'red-cross', 'blue-reason');
                        }
                    });
                });
            }
    
            let changeMode = false;
            function change() {
                const changeButton = document.querySelector("#change"); // The "Change Attendance" button
                const cells = document.querySelectorAll('.attendance-cell'); // Attendance cells
                setupCheckboxListeners()
                // Toggle the "Change" mode
                changeMode = !changeMode;
    
                if (changeMode) {
                    // Activate "Change" mode: highlight the button
                    changeButton.classList.add('active'); // Add a CSS class for styling
    
                    // Add click listeners to cells (for toggling attendance states)
                    cells.forEach(cell => {
                        cell.addEventListener('click', toggleAttendanceState);
                    });
                } else {
                    // Deactivate "Change" mode: reset the button
                    changeButton.classList.remove('active');
    
                    // Remove event listeners to prevent further changes
                    cells.forEach(cell => {
                        cell.removeEventListener('click', toggleAttendanceState);
                    });
                }
            }
    
            function toggleAttendanceState(event) {
                const cell = event.target;
                // if (lockedCells.has(cell)) return;
                const content = cell.textContent.trim();
                // Toggle between attendance states
                if (content === '✔') {
                    cell.textContent = '✘';  // Absent
                    cell.classList.remove('green-check');
                    cell.classList.add('red-cross');
                } else if (content === '✘') {
                    cell.textContent = 'p';  // Pending with reason
                    cell.classList.remove('red-cross');
                    cell.classList.add('blue-reason');
    
                } else if (content === 'p') {
                    cell.textContent = '✔';  // Present
                    cell.classList.remove('blue-reason');
                    cell.classList.add('green-check');
                } else {
                    cell.textContent = '';  // No selection (empty)
                    cell.classList.remove('green-check', 'red-cross', 'blue-reason');
    
                }
            }
            // Show popup
            let submitting = false;
            function openPopup() {
                popup = document.getElementById("fileUploaderPopup");
                popupTitle = document.getElementById("popupTitle");
                registrationForm = document.getElementById("registrationForm");
                submitBtn = document.getElementById("submitBtn");
                studentid = document.getElementById("student-id");
                studentid.style.display = 'none';
                submitting = !submitting;
    
                if (submitting) {
                    // Activate "Change" mode: highlight the button
                    submitBtn.classList.add('active'); // Add a CSS class for styling
                } else {
                    // Deactivate "Change" mode: reset the button
                    submitBtn.classList.remove('active');
                }
            
                // Set mode for file upload
                popupTitle.textContent = "File Upload";
                registrationForm.style.display = "none";
                submitBtn.onclick = uploadFiles;
            
                popup.style.display = "flex";
                document.getElementById('fileUploaderPopup').style.display = 'flex';
            }
    
            function openRegisterPopup() {
                popup = document.getElementById("fileUploaderPopup");
                popupTitle = document.getElementById("popupTitle");
                registrationForm = document.getElementById("registrationForm");
                submitBtn = document.getElementById("submitBtn");
                studentid = document.getElementById("student-id");
                studentid.style.display = 'block';
                // Set mode for student registration
                popupTitle.textContent = "Student Registration";
                registrationForm.style.display = "block";
                submitBtn.onclick = submitForm;
            
                popup.style.display = "flex";
            }
            // Close popup
            function closePopup() {
                const popup = document.getElementById("fileUploaderPopup");
                popup.style.display = "none";
                submitting = !submitting;
    
                if (submitting) {
                    // Activate "Change" mode: highlight the button
                    submitBtn.classList.add('active'); // Add a CSS class for styling
                } else {
                    // Deactivate "Change" mode: reset the button
                    submitBtn.classList.remove('active');
                }
            }

 
            function getSelectedDates() {
                // Collect all checked checkboxes and their dates
                const checkboxes = document.querySelectorAll('.column-checkbox');
                const selectedDates = [];
                checkboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        selectedDates.push(checkbox.getAttribute('data-date'));
                    }
                });
                return selectedDates;
            }
            function uploadFiles() {
                const selectedDates = getSelectedDates();
                const form = document.querySelector("form");
                const fileInput = form.querySelector('.file-input');
                const loader = document.querySelector('.loader');
                const files = fileInput.files;
    
                if (files.length === 0) {
                    alert("Please select files to upload!");
                    return;
                }
    
                const formData = new FormData();
                for (const file of files) {
                    formData.append('files', file);
                }
    
                // Append selected dates to FormData
                formData.append('selected_dates', JSON.stringify(selectedDates));
                formData.append('course_code', 'CSS324'); // Adjust dynamically if needed
                formData.append('time', new Date().toLocaleTimeString());
                
                const xhr = new XMLHttpRequest();
                xhr.open("POST", "http://192.168.0.225:5000/find", true);
                
                loader.style.display = "block";

                xhr.upload.addEventListener("progress", ({ loaded, total }) => {
                    const percentComplete = Math.floor((loaded / total) * 100);
                    console.log(`Progress: ${percentComplete}%`);
                });

                xhr.onload = () => {
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        alert("Upload successful!");
                        console.log(response);
                        // updateAttendanceTable(response.students_found, selectedDates);
                        fetchAndShowAttendance('CSS324',dates)
                        closePopup();
                    } else {
                        alert("Upload failed: " + xhr.responseText);
                    }
                    loader.style.display = "none";
                    
                };
    
                xhr.onerror = () => {
                    alert("An error occurred during the upload.");
                    loader.style.display = "none";
                };
    
                xhr.send(formData);
            }
    
            // Update attendance table dynamically
            function updateAttendanceTable(students, selectedDates) {
                const table = document.getElementById('attendance-table');
                if (!table) return;
    
                students.forEach(studentId => {
                    selectedDates.forEach(date => {
                        const cell = table.querySelector(`[data-student="${studentId}"][data-date="${date}"]`);
                        if (cell) {
                            cell.textContent = '✔';
                            cell.classList.remove('red-cross');
                            cell.classList.add('green-check');
                            
                        }
                    });
                });
            }
            const form = document.querySelector("form"),
            fileInput = document.querySelector(".file-input"), 
            progressArea = document.querySelector(".progress-area"),
            uploadedArea = document.querySelector(".uploaded-area"),
            submitButton = document.querySelector(".submit-btn");
    
            let uploadedFiles = []; // Store uploaded files
    
            // File Input Trigger
            form.addEventListener("click", () =>{
                fileInput.click();
            });
    
            // Handle File Input Change
            fileInput.onchange = ({target})=>{
                let file = target.files[0];
                if(file){
                    let fileName = file.name;
                    if(fileName.length >= 12){
                        let splitName = fileName.split('.');
                        fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
                    }
                    uploadFile(fileName, file);
                }
            }
    
            // Upload File Function
            function uploadFile(name, file){
                let xhr = new XMLHttpRequest();
                xhr.open("POST", "php/upload.php");
            
                // Handle Progress
                xhr.upload.addEventListener("progress", ({loaded, total}) =>{
                    let fileLoaded = Math.floor((loaded/total)*100);
                    let fileSize = (total / 1024).toFixed(2) + " KB";
                
                    let progressHTML = `
                        <li class="row">
                            <i class="fas fa-file-alt"></i>
                            <div class="content">
                                <div class="details">
                                    <span class="name">${name} * Uploading</span>
                                    <span class="percent">${fileLoaded}%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress" style="width:${fileLoaded}%"></div>
                                </div>
                            </div>
                        </li>`;
                    
                    progressArea.innerHTML = progressHTML;
                    
                    if(loaded == total){
                        uploadedFiles.push(name);
                        progressArea.innerHTML = "";
                        let uploadedHTML = `
                            <li class="row">
                                <div class="content upload">
                                    <i class="fas fa-file-alt"></i>
                                    <div class="details">
                                        <span class="name">${name} * Uploaded</span>
                                        <span class="size">${fileSize}</span>
                                    </div>
                                </div>
                                <span class="delete-btn" onclick="deleteFile(this, '${name}')">
                                    <i class="fas fa-trash"></i>
                                </span>
                            </li>`;
                        uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
                    }
                });
            
                let data = new FormData();
                data.append("file", file);
                xhr.send(data);
            }
    
            // Handle Submit Button
            submitButton.addEventListener("click", () => {
                if (uploadedFiles.length > 0) {
                    alert("Files submitted successfully!");
                } else {
                    alert("No files to submit!");
                }
            });
    
            // Delete File Function
            function deleteFile(element, fileName) {
                element.parentElement.remove();
                uploadedFiles = uploadedFiles.filter(file => file !== fileName);
            }
    
            function fetchAndShowAttendance(courseCode, dates) {
                fetch(`http://192.168.0.225:5000/get_attendance?course_code=${courseCode}`)
                    .then(response => response.json())
                    .then(data => {
                        renderAttendanceTable(data.students, dates);
                    })
                    .catch(err => {
                        console.error("Error fetching attendance:", err);
                        alert("Error fetching attendance data.");
                    });
            }
    
            function renderAttendanceTable(students, dates) {
                const attendanceDiv = document.getElementById('attendance');
                attendanceDiv.innerHTML = `
                    <h3>Attendance Table</h3>
                    <div class="table-container">
                        <table id="attendance-table">
                            <thead>
                                <tr>
                                    <th>Student ID</th>
                                    ${dates.map(date => `<th>${date}<br><input type="checkbox" class="column-checkbox" data-date="${date}" /></th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${Object.keys(students).map(studentId => {
                                    const student = students[studentId];
                                    return `
                                        <tr>
                                            <td>${studentId}</td>
                                            ${dates.map(date => {
                                                const status = student.attendance[date] || '✘'; // Default to '✘' if no status
                                                
                                                // Determine the class based on the status
                                                let statusClass = '';
                                                if (status === '✔') statusClass = 'green-check';
                                                else if (status === '✘') statusClass = 'red-cross';
                                                else if (status === 'p') statusClass = 'blue-reason';
    
                                                return `
                                                    <td 
                                                        class="attendance-cell ${statusClass}" 
                                                        data-student="${studentId}" 
                                                        data-date="${date}">
                                                        ${status}
                                                    </td>`;
                                            }).join('')}
                                        </tr>`;
                                }).join('')}
                            </tbody>
                        </table>
                    </div>
                    <div class="btn-container">
                        <button class="set-attendance-btn" onclick="submitAttendance()">Submit Attendance</button>
                        <button id="change" class="set-attendance-btn" onclick="change()">Change Attendance</button>
                        <button class="set-attendance-btn" id="submit-btn" onclick="openPopup()">Photo/Video attendance</button>
                    </div>`;
            }
            async function submitAttendance() {
                const cells = document.querySelectorAll('.attendance-cell');
                const loader = document.querySelector('.loader');
                const selectedDates = getSelectedDates(); // Selected dates from checkboxes
                const attendanceData = [];
                const courseCode = "CSS324"; // Replace with your actual course code
                
                loader.style.display = "block";

                cells.forEach(cell => {
                    const status = cell.textContent.trim(); // Attendance status
                    if (!status) return; // Skip empty cells
    
                    const studentId = cell.getAttribute('data-student');
                    const dateTime = cell.getAttribute('data-date'); // Full datetime
                    const [date, time] = dateTime.split(" "); // Split into date and time
    
                    // Only include data for selected dates
                    if (selectedDates.includes(dateTime)) {
                        attendanceData.push({
                            student_id: studentId,
                            date: date,
                            time: time,
                            status: status
                        });
                    }
                });
    
                // Send the formatted data to the backend
                try {
                    const response = await fetch('http://192.168.0.225:5000/submit_attendance', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            course_code: courseCode,
                            attendance: attendanceData
                        })
                    });
    
                    const result = await response.json();
                    if (response.ok) {
                        alert(result.message || "Attendance submitted successfully!");
                        lockCellsAfterSubmission();
                    } else {
                        alert(result.error || "Error submitting attendance.");
                    }
                } catch (error) {
                    console.error("Failed to submit attendance:", error);
                    alert("Network error while submitting attendance.");
                } finally{
                    loader.style.display = "none";
                }
            }
    
            // Locks cells after successful submission
            function lockCellsAfterSubmission() {
                const cells = document.querySelectorAll('.attendance-cell');
                cells.forEach(cell => {
                    if (cell.textContent.trim()) lockedCells.add(cell);
                });
            }
            async function submitForm() {
                const studentId = document.getElementById("student-id").value.trim();
                const files = fileInput.files;
            
                if (!studentId || files.length === 0) {
                    alert("Please enter your Student ID and upload at least one photo.");
                    return;
                }
            
                const formData = new FormData();
                formData.append("student_id", studentId);
            
                Array.from(files).forEach(file => {
                    formData.append("photos", file);
                });
                console.log(formData);
                const xhr = new XMLHttpRequest();
                xhr.open("POST", "http://192.168.0.225:5000/register", true);
    
                xhr.upload.addEventListener("progress", ({ loaded, total }) => {
                    const percentComplete = Math.floor((loaded / total) * 100);
                    console.log(`Progress: ${percentComplete}%`);
                });
    
                xhr.onload = () => {
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        alert("Upload successful!");
                        console.log(response);
                        closePopup();
                    } else {
                        alert("Upload failed: " + xhr.responseText);
                    }
                };
    
                xhr.onerror = () => {
                    alert("An error occurred during the upload.");
                };
    
                xhr.send(formData);
            }
    