
let subject_codes_to_sub_lists = null

function add_request()
{
    if (subject_codes_to_sub_lists == null)
        subject_codes_to_sub_lists = JSON.parse(document.getElementById("subs").innerText)

    // for (let key of Object.keys(subject_codes_to_sub_lists)) {
    //     console.log(key + " -> " + Object.values(subject_codes_to_sub_lists[key])[0])
    // }


}