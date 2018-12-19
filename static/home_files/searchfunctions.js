

function ClearSrchBox(formname) {
    workingForm = document.getElementById(formname);
    // if (workingForm.txtEtsuSrch.value == "Enter name or search term") {
    workingForm.txtetsusrch.value = "";
    //}
}
function ResetSrchBox(formname) {
    workingForm = document.getElementById(formname);
    if (workingForm.txtetsusrch.value == "") {
        workingForm.txtetsusrch.value = 'Search ETSU and People';
    }
}

function ClearLocalSrchBox(formname) {
    workingForm = document.getElementById(formname);
    // if (workingForm.txtEtsuSrch.value == "Enter name or search term") {
    workingForm.txtsitesrch.value = "";
    //}
}
function ResetLocalSrchBox(formname) {
    workingForm = document.getElementById(formname);
    if (workingForm.txtsitesrch.value == "") {
        workingForm.txtsitesrch.value = 'Search this Site';
    }
}
// this function allows the user to press the <enter> key when they are performing
// either a people search OR an ETSU search and it will execute the correct server side code
function checkEnter(btn, event) {

    if (document.all) {

        if (event.keyCode == 13) {

            var o = document.getElementById(btn);

            event.returnValue = false;

            event.cancel = true;

            o.click();

        }

    }

    else if (document.getElementById) {

        if (event.which == 13) {

            var o = document.getElementById(btn);

            event.returnValue = false;

            event.cancel = true;

            o.click();

        }

    }

    else if (document.layers) {

        if (event.which == 13) {

            var o = document.getElementById(btn);

            event.returnValue = false;

            event.cancel = true;

            o.click();

        }

    }

}

