import * as Yup from "yup";
import { useFormik } from "formik";
import { Link } from "react-router-dom";
import { useState } from "react";
import { FaEnvelope, FaLock, FaRegEye, FaRegEyeSlash } from "react-icons/fa6";
import InputField from "../components/InputField";
import SigninSVG from "../assets/SigninSVG.svg";
import FormErrors from "../components/FormErrors";

const Login = () => {
	const [showPassword, setShowPassword] = useState(false);
	const handleShowPassword = () => {
		setShowPassword(!showPassword);
	};

	// Validation with formik and yup
	const initialValues = {
		email: "",
		password: "",
	};

	const validationSchema = Yup.object({
		email: Yup.string()
			.email("Invalid email")
			.required("Email is required"),
		password: Yup.string()
			.required("Password is required")
			.min(8, "Must be at least 8 characters"),
	});

	const formik = useFormik({
		initialValues,
		validationSchema,
		onSubmit: (values) => {
			console.log(values);
		},
	});

	return (
		<div className="bg-gray-100 h-screen flex p-4">
			<div className="flex md:flex-row max-w-[1000px] justify-center items-center m-auto lg:p-20 rounded-3xl bg-white shadow-2xl flex-col p-7">
				{/* image container */}
				<div className="flex-1 flex h-full ">
					<img src={SigninSVG} alt="" />
				</div>

				<div className="flex-1 flex flex-col h-full items-center justify-center w-full">
					<h1 className="text-center text-3xl font-bold p-4 my-3">
						Sign in
					</h1>
					<form
						action=""
						onSubmit={formik.handleSubmit}
						className="flex flex-col gap-4 w-full max-w-[400px]"
					>
						<InputField
							type="email"
							name="email"
							id="email"
							placeholder="Email"
							onChange={formik.handleChange}
							value={formik.values.email}
							icon={<FaEnvelope />}
							pad
						/>

						{formik.touched.email && formik.errors.email ? (
							<FormErrors error={formik.errors.email} />
						) : null}

						<div className="flex flex-col relative w-full">
							<div className="flex">
								<InputField
									type={showPassword ? "text" : "password"}
									name="password"
									id="password"
									placeholder="Password"
									onChange={formik.handleChange}
									value={formik.values.password}
									icon={<FaLock />}
									pad
								/>

								{showPassword ? (
									<FaRegEyeSlash
										className="absolute right-2 flex self-center justify-center"
										onClick={handleShowPassword}
									/>
								) : (
									<FaRegEye
										className="absolute right-2 flex self-center justify-center"
										onClick={handleShowPassword}
									/>
								)}
							</div>

							{formik.touched.password &&
							formik.errors.password ? (
								<FormErrors error={formik.errors.password} />
							) : null}
						</div>

						<button className="flex m-auto my-5 p-4 px-8 rounded-lg bg-blue-500 hover:bg-blue-400 text-white">
							Log in
						</button>

						<div className="text-right">
							<Link
								to="/signup"
								className="text-right text-blue-500 hover:text-blue-400 underline"
							>
								Create an account
							</Link>
						</div>
					</form>
				</div>
			</div>
		</div>
	);
};

export default Login;
