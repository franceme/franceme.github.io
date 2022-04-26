title: BasePage

<h3><a href="{{url_for('index',_anchor='AboutMe')}}" id='AboutMe'>About Me</a></h3>

<p style="display:flex;">
<span style="width: 100%;  height: 120px;  display: flex;  flex-direction: column;">
    <img style="max-width:75%;min-width:50%;" src="/static/images/low_res.jpg" />
    <img style="max-width:75%;min-width:50%;" src="/static/images/VCard.svg" />
    </span>
    <span style="float:right;">
    	My Ph.D. research focuses on creating code analysis tools to assist developers by identifying cryptographic misuse in software repositories.
	My tools save developers time by using on-demand static code analysis to specifically scan for the cryptographic rules that may be broken.
	My tools also show higher precision than existing tools to ensure developers pay attention to the results.
	I also utilize several formats for my results to fit into many different DevOps tools and fit nicely into the development lifecycle.
	<br>
	<br>
    Focusing on the source of the vulnerabilities will provide better long-term solutions as opposed to continuing patching the issues.
    My application-focused research allows me to provide direct impact to current and upcoming vulnerabilities.
	{#
        I am a 3rd-year Ph.D. Computer Science student and am currently working on exciting projects.
        Currently, I am working with <a href="http://people.cs.vt.edu/danfeng/">Dr. Danfeng Yao</a>.
        <br>
        Previously I have worked in <a href="https://worldpay.com/">Worldpay from FIS</a> for several Internships (or Co-Ops) and have learned a lot through my various teams.
        <br>
	#}
        <br>
        <br>
        I enjoy working on side projects to learn new skills and techniques.
    </span>
</p>


<script>
window.onload = function () {
        var footer=document.getElementById('footer');
        footer.setAttribute("style",footer.getAttribute("style") + "bottom:0;");
}
</script>
