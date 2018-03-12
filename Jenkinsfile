properties([
	disableConcurrentBuilds(),
	parameters([
		string(defaultValue: '', description: '', name: 'branch'),
	]),
	pipelineTriggers([])
])

node("master") {
	
	stage ('Checkout from branch "${params.branch}" ') {
            try {
		sh "mkdir -p service"
		checkout([$class: 'GitSCM', branches: [[name: "${params.branch}"]], doGenerateSubmoduleConfigurations: true, extensions: [[
		$class: 'RelativeTargetDirectory', relativeTargetDir: "service"]], submoduleCfg: [], userRemoteConfigs: [[creadentialsId:
		'zweer1', url: "https://github.com/zweer1/service.git"]]])
	    } catch (exc) {
		error "Failed to checkout branch - ${params.branch}"
	}
	if (fileExists('/etc/systemd/system/counter.service')){
		echo 'counter.service exists doing restart'
		sh "sudo systemctl restart counter"
	} else {
		echo 'counter.service not exists'
		try {
		    stage ('Prepare the server to run the counter-service') {
		       sh "chmod +x /var/lib/jenkins/workspace/${env.JOB_NAME}/service/counter_config.sh"
		       sh 'sh -c "sudo ./service/counter_config.sh"'
	    	    }
		    stage ('Run the counter-service') {
		       sh "sudo systemctl enable counter && sudo systemctl restart counter"
		    }
		} catch (exc) {
	            error "Filed to deploy the counter_config.sh"
		}
		
        }
    }
}


