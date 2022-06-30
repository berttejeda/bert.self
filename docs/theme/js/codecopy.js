// const noteDiv = document.createElement("div")
// noteDiv.appendChild(document.createTextNode('copy'));
// noteDiv.setAttribute("class", "ribbon");

// const p = document.createElement("p");
// p.textContent = "test1";
// document.body.insertBefore(p, document.body.firstChild);

const copyToClipboard = str => {
  const el = document.createElement("textarea") // Create a <textarea> element
  el.value = str // Set its value to the string that you want copied
  el.setAttribute("readonly", "") // Make it readonly to be tamper-proof
  el.style.position = "absolute"
  el.style.left = "-9999px" // Move outside the screen to make it invisible
  document.body.appendChild(el) // Append the <textarea> element to the HTML document
  const selected =
    document.getSelection().rangeCount > 0 // Check if there is any content selected previously
      ? document.getSelection().getRangeAt(0) // Store selection if found
      : false // Mark as false to know no selection existed before
  el.select() // Select the <textarea> content
  document.execCommand("copy") // Copy - only works as a result of a user action (e.g. click events)
  document.body.removeChild(el) // Remove the <textarea> element
  if (selected) {
    // If a selection existed before copying
    document.getSelection().removeAllRanges() // Unselect everything on the HTML document
    document.getSelection().addRange(selected) // Restore the original selection
  }
}

function delay(time) {
  return new Promise(resolve => setTimeout(resolve, time));
}

// On-Click event for single-line codeblocks
function handleSingleLineCodeClick(evt) {
  // copy all of the code to the clipboard
  copyToClipboard(evt.target.innerText)
  var div = document.querySelector("div.md-dialog");
  var dataAttribute = div.getAttribute('data-md-state');
  if (dataAttribute === null) {
    div.setAttribute("data-md-state", "open");
    originalContent = div.innerHTML;
    div.innerHTML = "Copied to clipboard";
    div.style.color = "white"; 
    delay(2000).then(() => div.removeAttribute("data-md-state"));
  }

}  

/* Find all codeblocks not under elements with class '.highlight'
and not with class from-file
These are generally single-line codeblocks */
const singleline_codeblocks = document.querySelectorAll("code:not(.highlight > * code):not(.from-file)")
singleline_codeblocks.forEach(codeblock => {
  i = 0
  codeblock.setAttribute("id", "single-line-codeblock-" + i.toString());
  // codeblock.setAttribute("class", "md-clipboard");
  codeblock.setAttribute("class", "single-line-codeblock");
  codeblock.addEventListener("click", handleSingleLineCodeClick)
  i++
})  

