var mix = {
	data() {
		return {
			success: false,
			error: false,
			pollInterval: null,
			status: '',
			waitStatuses: [3, 4],
			errorStatus: 3,
			successStatus: 4,
		};
	},
	mounted() {
		this.fetchPaymentStatus();
		this.pollingPaymentStatus(paymentID);
	},
	methods: {
		fetchPaymentStatus(paymentID) {
			axios.defaults.xsrfCookieName = 'csrftoken';
			axios.defaults.xsrfHeaderName = 'X-CSRFToken';
			axios
				.get(`http://0.0.0.0:8000/api/payment/${paymentID}`, {
					headers: {
						Accept: 'application/json',
						'Content-Type': 'application/json',
						'X-Sessionid': this.getCookie('sessionid'),
					},
					withCredentials: true,
				})
				.then((response) => {
					this.status = response.data.status;
				})
				.catch((error) => {})
				.finally();
		},
		pollingPaymentStatus(paymentID) {
			const checkPaymentStatus = (paymentId) => {
				this.fetchPaymentStatus(paymentId);
				this.success = this.status === this.successStatus;
				this.error = this.status === this.errorStatus;
				if (this.success || this.error) {
					clearInterval(this.pollInterval);
				}
			};

			if (!this.waitStatuses.includes(this.status)) {
				this.pollInterval = setInterval(checkPaymentStatus, 5000, paymentID);
				setTimeout(() => {
					clearInterval(this.pollInterval);
					this.error = true;
				}, 300000);
			} else {
				this.success = this.status === this.successStatus;
				this.error = this.status === this.errorStatus;
			}
		},
	},
};
