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
	async mounted() {
		this.status = await this.fetchPaymentStatus(paymentID);
		await this.pollingPaymentStatus(paymentID);
	},
	methods: {
		async fetchPaymentStatus(paymentID) {
			try {
				resp = await this.axios.get(`/api/payment/${paymentID}`);
				return resp.data.status;
			} catch {}
		},
		async pollingPaymentStatus(paymentID) {
			const checkPaymentStatus = async (paymentId) => {
				this.status = await this.fetchPaymentStatus(paymentId);
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
