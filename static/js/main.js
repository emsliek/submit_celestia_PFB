{
    const api = {
        submit_pfb: "/submit_pfb"
    };

    const form = document.body.querySelector("form");

    // create transaction
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        document.getElementById("transaction_result").innerHTML = "Please wait...";

        let tx_form = {
            "message": form['message'].value,
            "gas_limit": form['gas_limit'].value,
            "fee": form['fee'].value,
        };

        console.log(tx_form)

        const connect = await fetch(api.submit_pfb, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(tx_form)
        }).then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Data error');
        }).then(data => {
            document.getElementById("transaction_result").innerHTML = "Submit Success";
            document.getElementById("transaction_info").hidden = false
            document.getElementById("tx_info_tx_hash").innerHTML = data.txhash;
            document.getElementById("tx_info_height").innerHTML = data.height;
            document.getElementById("tx_info_date").textContent = data.date;
            document.getElementById("tx_info_namespace_id").innerHTML = data.namespace_id;
            document.getElementById("tx_info_gas_used").innerHTML = data.gas_used;

            return data;
        }).catch(err => {
            document.getElementById("transaction_result").innerHTML = "Failed, Please make sure the celestia node is available and try again!";
        });
    });
}
