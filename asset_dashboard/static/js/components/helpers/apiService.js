import Cookies from 'js-cookie'

class ApiService {
  constructor({ onResponse }) {
    this.requestConfig = {
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFTOKEN': Cookies.get('csrftoken')
      },
      mode: 'same-origin'
    }
    
    this.onResponse = onResponse
  }
  
  parseErrorMessages(errors) {
    let errorMessage = ''

    errors.forEach(error => {
      for (const [key, value] of Object.entries(error)) {
        errorMessage += `Error for field: ${key}. ${value.join(' ')}`
      }
    })

    return {
      text: `An error occured saving the assets. ${errorMessage}`,
      tag: 'danger'
    }
  }
  
  setNewPhase(incomingPhaseId, outgoingPhaseId) {
    const data = {
      'new_phase_id': parseInt(incomingPhaseId),
      'old_phase_id': parseInt(outgoingPhaseId)
    }

    fetch(`/projects/phases/promote/assets/`, {
        ...this.requestConfig,
        method: 'POST',
        body: JSON.stringify(data)
    }).then((response) => {
      if (response.status == 201) {
        this.onResponse({
          text: 'Assets successfully promoted to new phase.',
          tag: 'success'
        })
        
        // Force redirect to the map with the new phase id
        location.assign(`/projects/phases/edit/${incomingPhaseId}/assets/`)
      } else {
        response.json().then(errors => {
          this.onResponse(this.parseErrorMessages(errors))
        })
      }
    }).catch(error => {
      console.error(error)

      this.onResponse({
        text: 'An error occurred promoting the assets. Please try again.',
        tag: 'danger'
      })
    })
  }
  
  saveCountywideSelection(isCountywide, phaseId) {
    const data = {
      'countywide': isCountywide,
      'phase_id': phaseId
    }

    fetch(`/projects/phases/assets/countywide/`, {
        ...this.requestConfig,
        method: 'POST',
        body: JSON.stringify(data)
    }).then((response) => {
      console.log('response')
      if (response.status == 201) {
        this.onResponse({
          text: 'Countywide succesfully changed for phase.',
          tag: 'success'
        })
        
        location.reload()
      } else {
        response.json().then(errors => {
          this.onResponse(this.parseErrorMessages(errors))
        })
        
        location.reload()
      }
    }).catch(error => {
      console.error(error)
      this.onResponse({
        text: 'An error occurred saving the countywide selection. Please try again.',
        tag: 'danger'
      })

      location.reload()
    })
  }
}

export default ApiService