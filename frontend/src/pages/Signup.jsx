import * as Yup from "yup";
import { useFormik } from "formik";
import { Link } from "react-router-dom";
import { useState } from "react";
import API_URL from "../config";
import axios from 'axios';

import {
	FaEnvelope,
	FaLock,
	FaRegEye,
	FaRegEyeSlash,
	FaRegUser,
} from "react-icons/fa6";
import InputField from "../components/InputField";
import SignupSVG from "../assets/SignupSVG.svg";
import FormErrors from "../components/FormErrors";

// ... Import statements ...

const Signup = () => {
	const [showPassword, setShowPassword] = useState(false);
	const handleShowPassword = () => {
	  setShowPassword(!showPassword);
	};
  
	// Validation with formik and yup
	const initialValues = {
	  firstName: "",
	  lastName: "",
	  email: "",
	  username: "",
	  password: "",
	  confirmPassword: "",
	};
  
	const validationSchema = Yup.object({
	  firstName: Yup.string().required("First name is required"),
	  lastName: Yup.string().required("Last name is required"),
	  email: Yup.string()
		.email("Invalid email")
		.required("Email is required"),
	  username: Yup.string().required("Username is required"),
	  password: Yup.string()
		.required("Password is required")
		.min(8, "Must be at least 8 characters"),
	  confirmPassword: Yup.string()
		.oneOf([Yup.ref("password"), null], "Passwords do not match")
		.required("Confirm password"),
	});
  
	// const formik = useFormik({
	//   initialValues,
	//   validationSchema,
	//   onSubmit: (values) => {
	// 	console.log(values);
	//   },
	// });
	const formik = useFormik({
		initialValues,
		validationSchema,
		onSubmit: async (values) => {
			console.log(values)
		  try {
			const csrfResponse = await axios.get('http://localhost:5000/get-token');
			console.log("CSRF Response: ", csrfResponse.data);
			const csrfToken = csrfResponse.data["X-CSRFToken"];
			console.log("CSRF Token: ", csrfToken);

			const headers = {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken
			};
			console.log(headers)
			const response = await axios.post('http://localhost:5000/signup', values, {
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrfToken
				}			}
			);
			console.log(response.data);
		  } catch (error) {
			console.error(error); // Handle errors
			// You can display an error message to the user
		  }
		},
	  });
	
  
	return (
	  <div className="bg-gray-100 h-screen flex p-4">
		<div className="flex md:flex-row max-w-[1000px] justify-center items-center m-auto lg:p-20 rounded-3xl bg-white shadow-2xl flex-col p-7">
		  <div className="flex-1 flex flex-col h-full items-center justify-center w-full">
			<h1 className="text-center text-3xl font-bold p-4 my-3">Sign up</h1>
			<form
			  action=""
			  onSubmit={formik.handleSubmit}
			  className="flex flex-col gap-4 w-full max-w-[400px]"
			>
			  <InputField
				type="text"
				name="firstName"
				id="firstName"
				placeholder="First Name"
				onChange={formik.handleChange}
				value={formik.values.firstName}
				icon={<FaRegUser />}
				pad
			  />
  
			  {formik.touched.firstName && formik.errors.firstName ? (
				<FormErrors error={formik.errors.firstName} />
			  ) : null}
  
			  <InputField
				type="text"
				name="lastName"
				id="lastName"
				placeholder="Last Name"
				onChange={formik.handleChange}
				value={formik.values.lastName}
				icon={<FaRegUser />}
				pad
			  />
  
			  {formik.touched.lastName && formik.errors.lastName ? (
				<FormErrors error={formik.errors.lastName} />
			  ) : null}
  
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
  
			  <InputField
				type="text"
				name="username"
				id="username"
				placeholder="Username"
				onChange={formik.handleChange}
				value={formik.values.username}
				icon={<FaRegUser />}
				pad
			  />
  
			  {formik.touched.username && formik.errors.username ? (
				<FormErrors error={formik.errors.username} />
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
  
				{formik.touched.password && formik.errors.password ? (
				  <FormErrors error={formik.errors.password} />
				) : null}
			  </div>
  
			  <div className="flex flex-col relative w-full">
				<InputField
				  type={showPassword ? "text" : "password"}
				  name="confirmPassword"
				  id="confirmPassword"
				  placeholder="Confirm Password"
				  onChange={formik.handleChange}
				  value={formik.values.confirmPassword}
				  icon={<FaLock />}
				  pad
				/>
				{formik.touched.confirmPassword && formik.errors.confirmPassword ? (
				  <FormErrors error={formik.errors.confirmPassword} />
				) : null}
			  </div>
  
			  <button className="flex m-auto my-5 p-4 px-8 rounded-lg bg-blue-500 hover:bg-blue-400 text-white">
				Register
			  </button>
  
			  <div className="text-right">
				Already have an account?{" "}
				<Link
				  to="/login"
				  className="text-right text-blue-500 hover:text-blue-400"
				>
				  Login
				</Link>
			  </div>
			</form>
		  </div>
  
		  {/* image container */}
		  <div className="flex-1 flex h-full">
			<img src={SignupSVG} alt="" />
		  </div>
		</div>
	  </div>
	);
  };
  
  export default Signup;
  